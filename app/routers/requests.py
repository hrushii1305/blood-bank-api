from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, auth, schemas
from app.database import get_db
from typing import Optional

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
def get_requests(
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.BloodRequest)
    if status:
        query = query.filter(models.BloodRequest.status == status)
    if urgency:
        query = query.filter(models.BloodRequest.urgency == urgency)
    return query.all()

@router.put("/requests/{id}/status")
def update_request_status(
    id: int,
    update: schemas.RequestStatusUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    request = db.query(models.BloodRequest).filter(
        models.BloodRequest.id == id
    ).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request.status = update.status
    db.commit()
    db.refresh(request)
    return {"message": "Status updated!", "request": request}