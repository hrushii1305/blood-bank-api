from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, auth, schemas
from app.database import get_db

router = APIRouter(tags=["Blood Requests"])

@router.post("/requests")
def create_request(
    request: schemas.BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    hospital = db.query(models.Hospital).filter(
        models.Hospital.id == request.hospital_id
    ).first()
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    new_request = models.BloodRequest(
        blood_group=request.blood_group,
        units_needed=request.units_needed,
        urgency=request.urgency,
        hospital_id=request.hospital_id
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/requests")
def get_requests(db: Session = Depends(get_db)):
    return db.query(models.BloodRequest).all()