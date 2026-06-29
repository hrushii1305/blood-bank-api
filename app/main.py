from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app import models
from app.database import engine
from app.routers import auth, donors, hospitals, requests, donations, inventory, emergency, stats

models.Base.metadata.create_all(bind=engine)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Blood Bank Management API",
    description="A REST API connecting blood donors with hospitals in need",
    version="1.0.0"
)

# Attach limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(donors.router)
app.include_router(hospitals.router)
app.include_router(requests.router)
app.include_router(donations.router)
app.include_router(inventory.router)
app.include_router(emergency.router)
app.include_router(stats.router)

@app.get("/")
def home():
    return {"message": "Blood Bank API 🩸"}

