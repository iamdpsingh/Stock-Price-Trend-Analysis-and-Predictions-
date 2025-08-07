from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional


def is_valid_object_id(v: str) -> bool:
    """Check if a string is a valid MongoDB ObjectId."""
    return ObjectId.is_valid(v)


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    hashed_password: str
    role: str = "user"
    is_active: bool = True

    @validator("id", pre=True, always=True)
    def validate_object_id(cls, v):
        if v is None:
            return v
        if isinstance(v, ObjectId):
            return str(v)
        if not is_valid_object_id(v):
            raise ValueError("Invalid ObjectId")
        return v

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "username": "exampleuser",
                "hashed_password": "...",
                "role": "user",
                "is_active": True,
            }
        }


class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"  # default to user, can be set to 'admin'


class UserOut(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    role: str
    is_active: bool

    @validator("id", pre=True, always=True)
    def validate_object_id(cls, v):
        if v is None:
            return v
        if isinstance(v, ObjectId):
            return str(v)
        if not is_valid_object_id(v):
            raise ValueError("Invalid ObjectId")
        return v

    class Config:
        allow_population_by_field_name = True


class Token(BaseModel):
    access_token: str
    token_type: str


class Stock(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    symbol: str
    name: str
    sector: str

    @validator("id", pre=True, always=True)
    def validate_object_id(cls, v):
        if v is None:
            return v
        if isinstance(v, ObjectId):
            return str(v)
        if not is_valid_object_id(v):
            raise ValueError("Invalid ObjectId")
        return v

    class Config:
        allow_population_by_field_name = True
