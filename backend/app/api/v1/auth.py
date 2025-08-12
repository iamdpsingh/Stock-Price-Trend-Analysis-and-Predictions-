from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import timedelta

from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_database
from app.core.config import settings

router = APIRouter()

# ---------------------
# Request/Response Models
# ---------------------

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------------
# Auth Endpoints
# ---------------------

@router.post("/signup", response_model=TokenResponse)
async def signup(user: SignupRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if email already exists
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password
    hashed_pw = hash_password(user.password)

    # Insert user into MongoDB
    user_doc = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed_pw,
        "created_at": None
    }
    await db["users"].insert_one(user_doc)

    # Create JWT
    token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.email}, expires_delta=token_expires)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if user exists
    user = await db["users"].find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create JWT
    token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user["email"]}, expires_delta=token_expires)
    return TokenResponse(access_token=token)
