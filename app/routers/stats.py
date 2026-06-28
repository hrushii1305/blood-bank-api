from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.database import get_db

router = APIRouter(tags=["Statistics"])

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    # Total donors
    total_donors = db.query(models.Donor).count()
    
    # Available donors
    available_donors = db.query(models.Donor).filter(
        models.Donor.is_available == True
    ).count()
    
    # Donors by blood group (GROUP BY!)
    blood_group_counts = db.query(
        models.Donor.blood_group,
        func.count(models.Donor.id)
    ).group_by(models.Donor.blood_group).all()
    
    # Convert to dictionary
    donors_by_blood_group = {bg: count for bg, count in blood_group_counts}
    
    # Total hospitals
    total_hospitals = db.query(models.Hospital).count()
    
    # Total requests
    total_requests = db.query(models.BloodRequest).count()
    
    # Critical requests
    critical_requests = db.query(models.BloodRequest).filter(
        models.BloodRequest.urgency == "critical"
    ).count()
    
    # Total donations
    total_donations = db.query(models.Donation).count()
    
    return {
        "total_donors": total_donors,
        "available_donors": available_donors,
        "donors_by_blood_group": donors_by_blood_group,
        "total_hospitals": total_hospitals,
        "total_requests": total_requests,
        "critical_requests": critical_requests,
        "total_donations": total_donations
    }
    
@router.get("/stats/city")
def stats_by_city(db: Session = Depends(get_db)):
    city_counts = db.query(
        models.Donor.city,
        func.count(models.Donor.id)
    ).group_by(models.Donor.city).all()
    
    return {
        "donors_by_city": {city: count for city, count in city_counts}
    }

@router.get("/stats/blood-group/{blood_group}")
def stats_for_blood_group(blood_group: str, db: Session = Depends(get_db)):
    # Total donors of this blood group
    total = db.query(models.Donor).filter(
        models.Donor.blood_group == blood_group
    ).count()
    
    # Available donors of this blood group
    available = db.query(models.Donor).filter(
        models.Donor.blood_group == blood_group,
        models.Donor.is_available == True
    ).count()
    
    return {
        "blood_group": blood_group,
        "total_donors": total,
        "available_donors": available
    }