from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        # JSONSchema for ObjectId is a string with 24 hex chars
        return {
            "type": "string",
            "pattern": "^[a-fA-F0-9]{24}$",
            "examples": ["507f1f77bcf86cd799439011"]
        }


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    hashed_password: str
    is_active: bool = True

    class Config:
        validate_by_name = True  # renamed from allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Stock(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    symbol: str
    name: str
    exchange: str

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    is_active: bool = True

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Token(BaseModel):
    access_token: str
    token_type: str
