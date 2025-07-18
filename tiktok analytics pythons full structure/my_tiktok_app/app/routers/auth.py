from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import uuid

from app.core.config import settings
from app.core.database import get_db, User

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None

class UserProfile(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    subscription_tier: str
    created_at: datetime

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str):
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """Hash password"""
    return pwd_context.hash(password)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # In a real app, you'd fetch from database
    # For now, return dummy user
    return {
        "id": user_id,
        "email": "user@example.com",
        "username": "demo_user",
        "subscription_tier": "premium"
    }

@router.post("/login")
async def login(user_data: UserLogin):
    """User login endpoint"""
    # For demo purposes, accept any email/password
    # In production, verify against database
    
    if user_data.email == "demo@example.com" and user_data.password == "password":
        access_token = create_access_token(data={"sub": "demo_user_id"})
        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": {
                    "id": "demo_user_id",
                    "email": user_data.email,
                    "username": "demo_user",
                    "subscription_tier": "premium"
                }
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
async def register(user_data: UserRegister):
    """User registration endpoint"""
    # In production, check if user already exists
    # For demo, always succeed
    
    user_id = str(uuid.uuid4())
    access_token = create_access_token(data={"sub": user_id})
    
    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user_id,
                "email": user_data.email,
                "username": user_data.username,
                "full_name": user_data.full_name,
                "subscription_tier": "free"
            }
        }
    }

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get user profile"""
    return {
        "success": True,
        "data": current_user
    }

@router.get("/subscriptions/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    plans = [
        {
            "id": "free",
            "name": "Free",
            "price": 0,
            "currency": "USD",
            "features": [
                "Basic analytics",
                "5 product searches per day",
                "Email support"
            ]
        },
        {
            "id": "pro",
            "name": "Pro",
            "price": 29,
            "currency": "USD",
            "features": [
                "Advanced analytics",
                "Unlimited searches",
                "Priority support",
                "API access"
            ]
        },
        {
            "id": "enterprise",
            "name": "Enterprise",
            "price": 99,
            "currency": "USD",
            "features": [
                "All Pro features",
                "Custom integrations",
                "Dedicated support",
                "White-label options"
            ]
        }
    ]
    
    return {"success": True, "data": plans} 