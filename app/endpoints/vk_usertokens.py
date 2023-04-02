from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.vk_usertokens import create_token, delete_token, get_all_tokens, get_token_by_id, update_token

from app.depends import get_db
from app.schemas.vk_usertoken import VKUsertokenBase


router = APIRouter()


@router.get("/usertokens", tags=["VK usertokens"])
async def get_all_vk_usertokens(
    db: Session = Depends(get_db)
):
    return get_all_tokens(db)


@router.get("/usertokens/{id}", tags=["VK usertokens"])
async def get_vk_usertoken_by_id(
    usertoken_id: int,
    db: Session = Depends(get_db)
):
    return get_token_by_id(db, usertoken_id)


@router.post("/usertokens/{id}", tags=["VK usertokens"])
async def create_vk_usertoken(
    usertoken: VKUsertokenBase,
    db: Session = Depends(get_db)
):
    return create_token(db, usertoken)


@router.put("/usertokens/{id}", tags=["VK usertokens"])
async def update_vk_usertoken(
    usertoken: VKUsertokenBase,
    usertoken_id: int,
    db: Session = Depends(get_db)
):
    return update_token(db, usertoken_id, usertoken)


@router.delete("/usertokens/{id}", tags=["VK usertokens"])
async def update_vk_usertoken(
    usertoken_id: int,
    db: Session = Depends(get_db)
):
    return delete_token(db, usertoken_id)