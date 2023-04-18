from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import vk_usertoken_methods

from app.depends import get_db
from app.schemas.vk_usertoken_schema import (
    VKUsertokenBase,
    VKUsertokenCreate,
    VKUsertokenResponse,
)
from app.security import auth


router = APIRouter()


@router.get("/usertokens", tags=["VK usertokens"])
async def get_all_vk_usertokens(
    auth: Annotated[bool, Depends(auth)],
    db: Session = Depends(get_db),
) -> list[VKUsertokenResponse]:
    return vk_usertoken_methods.get_all_tokens(db)


@router.get("/usertokens/{usertoken_id}", tags=["VK usertokens"])
async def get_vk_usertoken_by_id(
    auth: Annotated[bool, Depends(auth)],
    usertoken_id: int,
    db: Session = Depends(get_db),
) -> VKUsertokenResponse:
    return vk_usertoken_methods.get_token_by_id(db, usertoken_id)


@router.post("/usertokens", tags=["VK usertokens"])
async def create_vk_usertoken(
    auth: Annotated[bool, Depends(auth)],
    usertoken: VKUsertokenCreate,
    db: Session = Depends(get_db),
):
    return vk_usertoken_methods.create_token(db, usertoken)


@router.put("/usertokens", tags=["VK usertokens"])
async def update_vk_usertoken(
    auth: Annotated[bool, Depends(auth)],
    usertoken: VKUsertokenBase,
    usertoken_id: int,
    db: Session = Depends(get_db),
) -> VKUsertokenResponse:
    return vk_usertoken_methods.update_token(db, usertoken_id, usertoken)


@router.delete("/usertokens/{usertoken_id}", tags=["VK usertokens"])
async def delete_vk_usertoken(
    auth: Annotated[bool, Depends(auth)],
    usertoken_id: int,
    db: Session = Depends(get_db),
) -> None:
    return vk_usertoken_methods.delete_token(db, usertoken_id)
