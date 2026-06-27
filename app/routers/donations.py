from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models, auth, schemas
from app.database import get_db

router = APIRouter(tags=["Donations"])

@router.post("/donations")
def record_donation(
    donation: schemas.DonationCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    # Step 1: Check donor exists
    donor = db.query(models.Donor).filter(
        models.Donor.id == donation.donor_id
    ).first()
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    # Step 2: Check hospital exists
    hospital = db.query(models.Hospital).filter(
        models.Hospital.id == donation.hospital_id
    ).first()
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    # Step 3: Check 90-day eligibility
    if donor.last_donated is not None:
        last_date = datetime.strptime(donor.last_donated, "%Y-%m-%d")
        days_since = (datetime.now() - last_date).days
        if days_since < 90:
            raise HTTPException(
                status_code=400,
                detail=f"Donor must wait {90 - days_since} more days (90-day rule)"
            )
    
    # Step 4: Record the donation
    today = datetime.now().strftime("%Y-%m-%d")
    new_donation = models.Donation(
        donor_id=donation.donor_id,
        hospital_id=donation.hospital_id,
        blood_group=donor.blood_group,    # auto from donor!
        units=donation.units,
        donated_at=today                   # auto today!
    )
    db.add(new_donation)
    
    # Step 5: UPDATE donor stats!
    donor.last_donated = today
    donor.total_donations = donor.total_donations + 1
    
    db.commit()
    db.refresh(new_donation)
    
    return {
        "message": "🩸 Donation recorded successfully!",
        "donation_id": new_donation.id,
        "donor": donor.name,
        "blood_group": donor.blood_group,
        "units": donation.units,
        "donated_at": today,
        "donor_total_donations": donor.total_donations
    }