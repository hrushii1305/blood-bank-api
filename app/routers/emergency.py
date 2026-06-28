from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, auth, schemas
from app.database import get_db

router = APIRouter(tags=["Emergency"])

BLOOD_COMPATIBILITY = {
    "O-":  ["O-"],
    "O+":  ["O-", "O+"],
    "A-":  ["O-", "A-"],
    "A+":  ["O-", "O+", "A-", "A+"],
    "B-":  ["O-", "B-"],
    "B+":  ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
}

@router.post("/emergency")
def emergency_request(
    request: schemas.BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    # Verify hospital exists
    hospital = db.query(models.Hospital).filter(
        models.Hospital.id == request.hospital_id
    ).first()
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    # Create the blood request
    new_request = models.BloodRequest(
        blood_group=request.blood_group,
        units_needed=request.units_needed,
        urgency=request.urgency,
        hospital_id=request.hospital_id
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    # Find compatible + available + nearby donors
    compatible_types = BLOOD_COMPATIBILITY.get(request.blood_group, [])
    matched_donors = db.query(models.Donor).filter(
        models.Donor.blood_group.in_(compatible_types),
        models.Donor.is_available == True,
        models.Donor.city == hospital.city
    ).all()
    
    return {
        "message": "🚨 Emergency request created!",
        "request_id": new_request.id,
        "hospital": hospital.name,
        "hospital_city": hospital.city,
        "blood_needed": request.blood_group,
        "units_needed": request.units_needed,
        "urgency": request.urgency,
        "compatible_blood_types": compatible_types,
        "donors_found_nearby": len(matched_donors),
        "donors": matched_donors
    }