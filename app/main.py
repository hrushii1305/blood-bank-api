from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import auth, donors, hospitals, requests, donations, inventory



# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Blood Bank Management API",
    description="A REST API connecting blood donors with hospitals in need",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(donors.router)
app.include_router(hospitals.router)
app.include_router(requests.router)
app.include_router(donations.router)
app.include_router(inventory.router)
# Root endpoint
@app.get("/")
def home():
    return {"message": "Blood Bank API 🩸"}