from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, auth, schemas
from app.database import get_db

router = APIRouter(tags=["Inventory"])

# Add or update blood stock
@router.post("/inventory")
def update_inventory(
    item: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    # Check hospital exists
    hospital = db.query(models.Hospital).filter(
        models.Hospital.id == item.hospital_id
    ).first()
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if this hospital+blood_group already exists
    existing = db.query(models.BloodInventory).filter(
        models.BloodInventory.hospital_id == item.hospital_id,
        models.BloodInventory.blood_group == item.blood_group
    ).first()
    
    if existing:
        # Update existing stock
        existing.units = item.units
        existing.updated_at = today
        db.commit()
        db.refresh(existing)
        return {"message": "Stock updated!", "inventory": existing}
    else:
        # Create new stock entry
        new_item = models.BloodInventory(
            hospital_id=item.hospital_id,
            blood_group=item.blood_group,
            units=item.units,
            updated_at=today
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"message": "Stock added!", "inventory": new_item}

# View all inventory
@router.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return db.query(models.BloodInventory).all()

# Shortage alerts (units < 5)
@router.get("/inventory/shortage")
def get_shortages(db: Session = Depends(get_db)):
    shortages = db.query(models.BloodInventory).filter(
        models.BloodInventory.units < 5
    ).all()
    
    return {
        "alert": "⚠️ Blood Shortage Alert",
        "critical_count": len(shortages),
        "shortages": shortages
    }