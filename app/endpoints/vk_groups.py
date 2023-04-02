from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.vk_groups import create_group, delete_group, get_all_groups, get_group_by_id, get_groups_by_token_id, update_group

from app.depends import get_db
from app.schemas.vk_group import VKGroupBase, VKGroupCreate


router = APIRouter()


@router.get("/groups", tags=["VK groups"])
async def get_all_vk_groups(
    db: Session = Depends(get_db)
):
    return get_all_groups(db)


@router.get("/groups/{id}", tags=["VK groups"])
async def get_vk_group_by_id(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_group_by_id(db, group_id)


@router.get("/groups/by_token/{id}", tags=["VK groups"])
async def get_vk_groups_by_token_id(
    token_id: int,
    db: Session = Depends(get_db)
):
    return get_groups_by_token_id(db, token_id)


@router.post("/groups", tags=["VK groups"])
async def create_vk_group(
    group: VKGroupCreate,
    db: Session = Depends(get_db)
):
    return create_group(db, group)


@router.put("/groups/{id}", tags=["VK groups"])
async def update_vk_group(
    # TODO: Not working. Needs fix.

    group: VKGroupBase,
    group_id: int,
    db: Session = Depends(get_db)
):
    return update_group(db, group_id, group)


@router.delete("/groups/{id}", tags=["VK groups"])
async def delete_vk_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    return delete_group(db, group_id)