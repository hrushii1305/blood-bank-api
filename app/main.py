from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app import models
from app.database import engine
from fastapi import Request
from fastapi.responses import JSONResponse
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

from app.logger import logger

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "An internal error occurred. Please try again later."}
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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Blood Bank API"}