from app.db.database import user_collection
from app.db.schemas import UserCreate, UserOut
from app.core.security import get_password_hash
from bson.objectid import ObjectId


async def get_user_by_username(username: str):
    user = await user_collection.find_one({"username": username})
    return user


async def get_user_by_id(user_id):
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    user = await user_collection.find_one({"_id": user_id})
    return user


async def create_user(user: UserCreate) -> UserOut:
    user_dict = user.dict()
    password_plain = user_dict.pop("password")
    user_dict["hashed_password"] = get_password_hash(password_plain)
    user_dict.setdefault("role", "user")
    user_dict["is_active"] = True
    result = await user_collection.insert_one(user_dict)
    created_user = await get_user_by_id(result.inserted_id)
    return UserOut(**created_user)


async def update_user_role(username: str, new_role: str):
    # Example utility - update user's role
    update_result = await user_collection.update_one(
        {"username": username},
        {"$set": {"role": new_role}},
    )
    return update_result.modified_count > 0


# Further CRUD operations for stocks, groups, transactions etc. to be added similarly.
