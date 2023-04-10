from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.vk_groups import create_group, create_group_source, delete_group, get_all_groups, get_group_by_id, get_group_sources, get_groups_by_token_id, update_group

from app.depends import get_db
from app.schemas.vk_group import VKGroupBase, VKGroupCreate, VKGroupRequest
from app.schemas.vk_groups_sources import VKGroupSourceBase
from app.crud import CRUD


router = APIRouter(tags=["VK groups"])


@router.get("/groups")
async def get_all_vk_groups(
    db: Session = Depends(get_db)
):
    return CRUD.vk_groups.get_all_groups(db)


@router.get("/groups/{id}")
async def get_vk_group_by_id(
    group_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.vk_groups.get_group_by_id(db, group_id)


@router.get("/groups/by_token/{id}")
async def get_vk_groups_by_token_id(
    token_id: int,
    db: Session = Depends(get_db)
):
    return get_groups_by_token_id(db, token_id)


@router.post("/groups")
async def create_vk_group(
    group: VKGroupRequest,
    db: Session = Depends(get_db)
):
    return await CRUD.vk_groups.create_group(db, group)


@router.put("/groups/{id}")
async def update_vk_group(
    # TODO: Not working. Needs fix.

    group: VKGroupBase,
    group_id: int,
    db: Session = Depends(get_db)
):
    return update_group(db, group_id, group)


@router.delete("/groups/{id}")
async def delete_vk_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    return delete_group(db, group_id)


@router.get("/groups/sources/{group_id}")
async def get_vk_group_sources(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_group_sources(db, group_id)


@router.post("/groups/sources")
async def create_vk_group_sources(
    group_source: VKGroupSourceBase,
    db: Session = Depends(get_db)
):
    return create_group_source(db, group_source)