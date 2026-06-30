from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, auth, schemas
from app.database import get_db
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(tags=["Authentication"])

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed = auth.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {user.username} registered!"}

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = auth.create_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not auth.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = auth.create_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}