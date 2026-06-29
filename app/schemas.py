from pydantic import BaseModel, validator
from typing import Optional

# ─── User Schemas ───
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# ─── Donor Schemas ───
class Donor(BaseModel):
    name: str
    blood_group: str
    city: str
    state: str                          # NEW
    phone: str
    age: int
    weight: int                         # NEW
    is_available: bool = True

    @validator('blood_group')
    def valid_blood_group(cls, v):
        valid = ['A+','A-','B+','B-','O+','O-','AB+','AB-']
        if v not in valid:
            raise ValueError(f'Must be one of {valid}')
        return v

    @validator('phone')
    def valid_phone(cls, v):
        if not v.isdigit():
            raise ValueError('Phone must contain only digits')
        if len(v) != 10:
            raise ValueError('Phone must be 10 digits')
        return v

    @validator('age')
    def valid_age(cls, v):
        if v < 18 or v > 65:
            raise ValueError('Donor age must be between 18 and 65')
        return v

    @validator('weight')
    def valid_weight(cls, v):
        if v < 50:
            raise ValueError('Donor weight must be at least 50kg')
        return v

class DonorUpdate(BaseModel):
    is_available: Optional[bool] = None
    last_donated: Optional[str] = None
    total_donations: Optional[int] = None

# ─── Hospital Schemas ───
class HospitalCreate(BaseModel):
    name: str
    city: str
    phone: str
    email: str

# ─── Blood Request Schemas ───
class BloodRequestCreate(BaseModel):
    blood_group: str
    units_needed: int
    urgency: str
    hospital_id: int
    
    
class DonationCreate(BaseModel):
    donor_id: int
    hospital_id: int
    units: int
    
class InventoryUpdate(BaseModel):
    hospital_id: int
    blood_group: str
    units: int
    
class RequestStatusUpdate(BaseModel):
    status: str