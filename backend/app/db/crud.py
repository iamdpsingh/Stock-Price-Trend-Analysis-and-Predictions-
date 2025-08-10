from bson.objectid import ObjectId
from app.db.database import user_collection, stock_collection, group_collection 
from app.db.schemas import UserCreate, UserOut, GroupCreate
from app.core.security import get_password_hash


# ---------------- USER CRUD ---------------- #

async def get_user_by_username(username: str):
    return await user_collection.find_one({"username": username})


async def get_user_by_id(user_id):
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return await user_collection.find_one({"_id": user_id})


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
    result = await user_collection.update_one(
        {"username": username},
        {"$set": {"role": new_role}},
    )
    return result.modified_count > 0


# ---------------- STOCK CRUD ---------------- #

async def update_or_create_stock(stock_data: dict):
    symbol = stock_data.get("symbol")
    if not symbol:
        return False
    existing = await stock_collection.find_one({"symbol": symbol})
    if existing:
        await stock_collection.update_one({"symbol": symbol}, {"$set": stock_data})
    else:
        await stock_collection.insert_one(stock_data)
    return True


async def follow_stock(username: str, symbol: str) -> bool:
    result = await user_collection.update_one(
        {"username": username},
        {"$addToSet": {"followed_stocks": symbol}},
    )
    return result.modified_count > 0


async def unfollow_stock(username: str, symbol: str) -> bool:
    result = await user_collection.update_one(
        {"username": username},
        {"$pull": {"followed_stocks": symbol}},
    )
    return result.modified_count > 0


async def list_stocks_by_search(query: str):
    cursor = stock_collection.find({"$text": {"$search": query}}).limit(20)
    return await cursor.to_list(length=20)


# ---------------- GROUP CRUD ---------------- #

async def create_group(username: str, group: GroupCreate):
    """Create a new group and set current user as the creator and first member."""
    group_data = group.dict()
    group_data["members"] = [username]
    existing = await group_collection.find_one({"name": group_data["name"]})
    if existing:
        return None  # group with same name already exists
    result = await group_collection.insert_one(group_data)
    if result.inserted_id:
        group_data["_id"] = str(result.inserted_id)
        return group_data
    return None


async def list_groups(username: str):
    """List all groups where current user is a member."""
    cursor = group_collection.find({"members": username})
    groups = []
    async for group in cursor:
        group["_id"] = str(group["_id"])
        groups.append(group)
    return groups



# Further CRUD operations for stocks, groups, transactions etc. to be added similarly.
