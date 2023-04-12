from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import vk_usertoken_methods
from app.depends import get_db
from app.models.vk_usertoken_model import VKUsertokenModel
from app.schemas.vk_group_schema import VKGroupExternal
from app.schemas.vk_usertoken_schema import VKUsertokenCreate
from app.utils.vk_api_wrapper.vk_api_wrapper import VKAPIWrapper
from app.utils.aes_tools.aes_cipher import aes_tools


router = APIRouter()


# TODO: return schema
@router.get("/vk_api/groups", tags=["VK API"])
async def get_groups_list(
    usertoken_id: int,
    passphrase: str,
    db: Session = Depends(get_db)
):
    enc_token = vk_usertoken_methods.get_token_by_id(db, usertoken_id).token
    dec_token = aes_tools.decrypt(enc_token, passphrase)

    vk_api = VKAPIWrapper(dec_token)
    
    try:
        groups = await vk_api.get_groups()
    except:
        raise HTTPException(
            detail="An error occured.",
            status_code=500
        )

    return groups


@router.get("/vk_api/groups/{group_id}", tags=["VK API"])
async def get_group_by_id(
    usertoken_id: int,
    passphrase: str,
    group_id: int,
    db: Session = Depends(get_db)
) -> VKGroupExternal:
    enc_token = vk_usertoken_methods.get_token_by_id(db, usertoken_id).token
    dec_token = aes_tools.decrypt(enc_token, passphrase)

    vk_api = VKAPIWrapper(dec_token)
    
    try:
        group = await vk_api.get_group_by_id(group_id)
    except:
        raise HTTPException(
            detail="An error occured.",
            status_code=500
        )

    return group