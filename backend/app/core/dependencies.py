from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.connection import mongodb_client
from app.core.security import decode_access_token

# OAuth2 scheme for FastAPI docs and token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------------
# Database Dependency
# -------------------------------
async def get_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Dependency to yield a MongoDB database instance for routes.
    Example usage:
        async def route(db: AsyncIOMotorDatabase = Depends(get_database)):
            ...
    """
    yield mongodb_client.db


# -------------------------------
# Authenticated User Dependency
# -------------------------------
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Dependency that extracts the current user from a JWT token.
    Raises 401 if the token is invalid/expired or the user is not found.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = await db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# -------------------------------
# Admin User Dependency (Optional RBAC)
# -------------------------------
async def get_admin_user(
    current_user: dict = Depends(get_current_user)
):
    """
    Ensures the current user has admin role.
    Modify the logic based on your role storage.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
