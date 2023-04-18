from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import CRUD

from app.depends import get_db
from app.schemas.vk_group_schema import VKGroupBase, VKGroupCreate, VKGroupRequest
from app.schemas.vk_group_source_schema import VKGroupSourceBase
from app.crud import CRUD
from app.security import auth


router = APIRouter(tags=["VK groups"])


@router.get("/groups")
async def get_all_vk_groups(
    auth: Annotated[bool, Depends(auth)], db: Session = Depends(get_db)
):
    return CRUD.vk_group_methods.get_all_groups(db)


@router.get("/groups/{group_id}")
async def get_vk_group_by_id(
    auth: Annotated[bool, Depends(auth)], group_id: int, db: Session = Depends(get_db)
):
    result = CRUD.vk_group_methods.get_group_by_id(db, group_id)

    if result:
        return result
    else:
        raise HTTPException(status_code=404)


@router.get("/groups/by_token/{token_id}")
async def get_vk_groups_by_token_id(
    auth: Annotated[bool, Depends(auth)], token_id: int, db: Session = Depends(get_db)
):
    result = CRUD.vk_group_methods.get_groups_by_token_id(db, token_id)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404)


@router.post("/groups")
async def create_vk_group(
    auth: Annotated[bool, Depends(auth)],
    group: VKGroupRequest,
    db: Session = Depends(get_db),
):
    return await CRUD.vk_group_methods.create_group(db, group)


@router.put("/groups/{group_id}")
async def update_vk_group(
    auth: Annotated[bool, Depends(auth)],
    group: VKGroupBase,
    group_id: int,
    db: Session = Depends(get_db),
):
    result = CRUD.vk_group_methods.update_group(db, group_id, group)

    if result:
        return result
    else:
        raise HTTPException(status_code=404)


@router.delete("/groups/{group_id}")
async def delete_vk_group(
    auth: Annotated[bool, Depends(auth)], group_id: int, db: Session = Depends(get_db)
):
    result = CRUD.vk_group_methods.delete_group(db, group_id)

    if result:
        return result
    else:
        raise HTTPException(status_code=404)


@router.get("/groups/sources/{group_id}")
async def get_vk_group_sources(
    auth: Annotated[bool, Depends(auth)], group_id: int, db: Session = Depends(get_db)
):
    result = CRUD.vk_group_methods.get_group_sources(db, group_id)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404)


@router.get("/groups/posts/all")
async def get_all_vk_groups_posts(
    auth: Annotated[bool, Depends(auth)], db: Session = Depends(get_db)
):
    return CRUD.vk_group_methods.get_all_groups_posts(db)


@router.get("/groups/posts/{group_id}")
async def get_vk_group_posts(
    auth: Annotated[bool, Depends(auth)], group_id: int, db: Session = Depends(get_db)
):
    return CRUD.vk_group_methods.get_group_posts(db, group_id)


@router.post("/groups/sources")
async def attach_sources_to_group(
    auth: Annotated[bool, Depends(auth)],
    group_sources: list[VKGroupSourceBase],
    db: Session = Depends(get_db),
):
    return CRUD.vk_group_methods.create_group_sources(db, group_sources)


@router.delete("/groups/{group_id}/sources/{source_id}")
async def detach_source_from_group(
    auth: Annotated[bool, Depends(auth)],
    group_id: int,
    source_id: int,
    db: Session = Depends(get_db),
):
    return CRUD.vk_group_methods.delete_group_source(db, group_id, source_id)
