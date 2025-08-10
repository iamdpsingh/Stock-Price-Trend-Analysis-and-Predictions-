from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.security import get_current_user
from app.db.schemas import GroupCreate, GroupOut
from app.db.crud import create_group, list_groups  # You need to implement these in crud.py accordingly

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=GroupOut)
async def create_new_group(group: GroupCreate, current_user=Depends(get_current_user)):
    created = await create_group(current_user["username"], group)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create group")
    return created

@router.get("/", response_model=List[GroupOut])
async def get_groups(current_user=Depends(get_current_user)):
    groups = await list_groups(current_user["username"])
    return groups
