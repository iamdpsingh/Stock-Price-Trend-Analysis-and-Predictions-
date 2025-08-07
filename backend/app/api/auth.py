from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.db.database import user_collection
from app.db.schemas import UserCreate, UserOut, Token
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    if await user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["is_active"] = True
    result = await user_collection.insert_one(user_dict)
    new_user = await user_collection.find_one({"_id": result.inserted_id})
    return UserOut(**new_user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(request: Request):
    # JWT is stateless: logout is frontend-only (remove from storage)
    return {"msg": "Logout successful. Remove the token on client side."}
