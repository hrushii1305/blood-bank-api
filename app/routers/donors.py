from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app import models, auth, schemas
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
    db: Session = Depends(get_db)
):
    query = db.query(models.Donor)
    if blood_group:
        query = query.filter(models.Donor.blood_group == blood_group)
    if city:
        query = query.filter(models.Donor.city == city)
    return query.all()

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
    donor = db.query(models.Donor).filter(models.Donor.id == id).first()
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor

@router.post("/donors")
def register_donor(
    donor: schemas.Donor,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    new_donor = models.Donor(
        name=donor.name,
        blood_group=donor.blood_group,
        city=donor.city,
        state=donor.state,          # NEW
        phone=donor.phone,
        age=donor.age,
        weight=donor.weight         # NEW
    )
    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return new_donor


@router.put("/donors/{id}")
def update_donor(
    id: int,
    donor: schemas.DonorUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    db_donor = db.query(models.Donor).filter(models.Donor.id == id).first()
    if db_donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    if donor.is_available is not None:
        db_donor.is_available = donor.is_available
    db.commit()
    db.refresh(db_donor)
    return db_donor

@router.delete("/donors/{id}")
def delete_donor(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    donor = db.query(models.Donor).filter(models.Donor.id == id).first()
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    db.delete(donor)
    db.commit()
    return {"message": f"Donor {id} deleted by {current_user}!"}