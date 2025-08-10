from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional, List


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
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
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
    sector: Optional[str] = ""

    class Config:
        allow_population_by_field_name = True

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class GroupOut(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: str
    members: List[str] = []

