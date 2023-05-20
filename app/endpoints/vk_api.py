from io import BytesIO
from typing import Annotated, Union

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud import CRUD, vk_usertoken_methods
from app.depends import get_db
from app.schemas.vk_group_schema import VKGroupExternal
from app.security import auth
from app.utils.aes_tools.aes_cipher import aes_tools
from app.utils.img_gen.img_gen import generate_image
from app.utils.vk_api_wrapper.vk_api_wrapper import VKAPIWrapper

router = APIRouter(tags=["VK API"])


# TODO: return schema
@router.get("/vk_api/groups")
async def get_groups_list(
    auth: Annotated[bool, Depends(auth)],
    usertoken_id: int,
    passphrase: str,
    db: Session = Depends(get_db),
):
    enc_token = vk_usertoken_methods.get_token_by_id(db, usertoken_id).token
    dec_token = aes_tools.decrypt(enc_token, passphrase)

    vk_api = VKAPIWrapper(dec_token)

    try:
        groups = await vk_api.get_groups()
    except:
        raise HTTPException(detail="An error occured.", status_code=500)

    return groups


@router.get("/vk_api/groups/{group_id}")
async def get_group_by_id(
    auth: Annotated[bool, Depends(auth)],
    usertoken_id: int,
    passphrase: str,
    group_id: int,
    db: Session = Depends(get_db),
) -> VKGroupExternal:
    enc_token = vk_usertoken_methods.get_token_by_id(db, usertoken_id).token
    dec_token = aes_tools.decrypt(enc_token, passphrase)

    vk_api = VKAPIWrapper(dec_token)

    try:
        group = await vk_api.get_group_by_id(group_id)
    except:
        raise HTTPException(detail="An error occured.", status_code=500)

    return group


@router.post("/vk_api/post")
async def post(
    auth: Annotated[bool, Depends(auth)],
    title: str = Form(),
    description: str = Form(),
    source: Union[str, None] = Form(None),
    source_url: Union[str, None] = Form(None),
    image: UploadFile = File(),
    usertoken_id: int = Form(),
    passphrase: str = Form(),
    group_id: int = Form(),
    publish_date: Union[int, None] = Form(None),
    db: Session = Depends(get_db),
):
    enc_token = vk_usertoken_methods.get_token_by_id(db, usertoken_id).token
    dec_token = aes_tools.decrypt(enc_token, passphrase)

    vk_api = VKAPIWrapper(dec_token)

    try:
        group_vk_id = CRUD.vk_group_methods.get_group_by_id(db, group_id).vk_id
    except:
        raise HTTPException(
            status_code=500, detail=f"Group with ID {group_id} does not exist."
        )

    image_bytes = image.file.read()

    if source_url:
        message = f"{title}%0A%0A{description}%0A%0A{source_url}"
    else:
        message = f"{title}%0A%0A{description}"

    await vk_api.create_post(
        group_id=group_vk_id,
        message=message,
        copyright=source_url,
        image=image_bytes,
        image_filename="image.png",
        publish_date=publish_date,
    )
