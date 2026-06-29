from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app import models, auth, schemas, crud
from app.database import get_db

router = APIRouter(tags=["Donors"])

# Blood compatibility map
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

@router.get("/donors")
def get_donors(
    blood_group: Optional[str] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_donors(db, blood_group, city, skip, limit)

@router.get("/donors/match/{blood_group}")
def match_donors(
    blood_group: str,
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    compatible_types = BLOOD_COMPATIBILITY.get(blood_group)
    if compatible_types is None:
        raise HTTPException(status_code=400, detail="Invalid blood group")
    
    query = db.query(models.Donor).filter(
        models.Donor.blood_group.in_(compatible_types),
        models.Donor.is_available == True
    )
    if city:
        query = query.filter(models.Donor.city == city)
    
    matches = query.all()
    return {
        "patient_needs": blood_group,
        "compatible_blood_types": compatible_types,
        "available_donors": matches,
        "total_matches": len(matches)
    }

@router.get("/donors/{id}")
def get_donor(id: int, db: Session = Depends(get_db)):
    donor = crud.get_donor(db, id)
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor

@router.post("/donors")
def register_donor(
    donor: schemas.Donor,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud.create_donor(db, donor)

@router.put("/donors/{id}")
def update_donor(
    id: int,
    donor: schemas.DonorUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    if donor.is_available is None:
        raise HTTPException(status_code=400, detail="No availability value provided")
    
    updated = crud.update_donor_availability(db, id, donor.is_available)
    if updated is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    return updated

@router.delete("/donors/{id}")
def delete_donor(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    deleted = crud.delete_donor(db, id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    return {"message": f"Donor {id} deleted by {current_user}!"}

@router.put("/donors/{id}/toggle")
def toggle_availability(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    donor = crud.get_donor(db, id)
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    donor.is_available = not donor.is_available
    db.commit()
    db.refresh(donor)
    return {"message": f"Availability toggled to {donor.is_available}", "donor": donor}