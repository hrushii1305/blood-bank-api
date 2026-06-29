from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas

# ─── DONOR CRUD ───

def get_donor(db: Session, donor_id: int):
    return db.query(models.Donor).filter(models.Donor.id == donor_id).first()

def get_donors(
    db: Session,
    blood_group: Optional[str] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.Donor)
    if blood_group:
        query = query.filter(models.Donor.blood_group == blood_group)
    if city:
        query = query.filter(models.Donor.city == city)
    return query.offset(skip).limit(limit).all()

def create_donor(db: Session, donor: schemas.Donor):
    new_donor = models.Donor(
        name=donor.name,
        blood_group=donor.blood_group,
        city=donor.city,
        state=donor.state,
        phone=donor.phone,
        age=donor.age,
        weight=donor.weight
    )
    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return new_donor

def update_donor_availability(db: Session, donor_id: int, is_available: bool):
    donor = get_donor(db, donor_id)
    if donor:
        donor.is_available = is_available
        db.commit()
        db.refresh(donor)
    return donor

def delete_donor(db: Session, donor_id: int):
    donor = get_donor(db, donor_id)
    if donor:
        db.delete(donor)
        db.commit()
    return donor

