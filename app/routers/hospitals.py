from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, auth, schemas
from app.database import get_db

router = APIRouter(tags=["Hospitals"])

@router.post("/hospitals")
def create_hospital(
    hospital: schemas.HospitalCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    new_hospital = models.Hospital(
        name=hospital.name,
        city=hospital.city,
        phone=hospital.phone,
        email=hospital.email
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital

@router.get("/hospitals")
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(models.Hospital).all()

@router.get("/hospitals/{id}")
def get_hospital(id: int, db: Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == id).first()
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital