from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.db.schemas import UserCreate, UserOut, Token
from app.db.crud import get_user_by_username, create_user
from app.core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    admin_required,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    created_user = await create_user(user)
    return created_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user.get("role", "user")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    # Stateless JWT logout (inform frontend to remove token)
    return {"msg": "Logout successful. Please remove token on client side."}


# Example admin-only route (Day 4 Admin feature)
@router.get("/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(admin_required)):
    return {"msg": f"Welcome to the admin dashboard, {current_user['username']}"}


# Example route requiring any authenticated user:
@router.get("/user/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "role": current_user["role"]}
