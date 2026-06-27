from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    blood_group = Column(String)
    city = Column(String)
    state = Column(String)              # NEW
    phone = Column(String)
    age = Column(Integer)
    weight = Column(Integer)            # NEW
    is_available = Column(Boolean, default=True)
    last_donated = Column(String, default=None)      # NEW
    total_donations = Column(Integer, default=0)     # NEW
    
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
class Hospital(Base):
    __tablename__ = "hospitals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    phone = Column(String)
    email = Column(String)
    
from sqlalchemy import ForeignKey

class BloodRequest(Base):
    __tablename__ = "blood_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    blood_group = Column(String)
    units_needed = Column(Integer)
    urgency = Column(String)
    status = Column(String, default="pending")
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    
class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    blood_group = Column(String)
    units = Column(Integer)
    donated_at = Column(String)
    
class BloodInventory(Base):
    __tablename__ = "blood_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    blood_group = Column(String)
    units = Column(Integer, default=0)
    updated_at = Column(String)