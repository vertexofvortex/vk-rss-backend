from io import BytesIO
from typing import Annotated

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


# @router.post("/vk_api/post")
# async def create_post(
#     auth: Annotated[bool, Depends(auth)],
#     title: str = Form(),
#     description: str = Form(),
#     source: str = Form(),
#     source_url: str = Form(),
#     image: UploadFile = File(),
#     logo: UploadFile = Form(),
#     usertoken_id: int = Form(),
#     passphrase: str = Form(),
#     group_id: int = Form(),
#     db: Session = Depends(get_db),
# ):
#     enc_token = vk_usertoken_methods.get_token_by_id(db, usertoken_id).token
#     dec_token = aes_tools.decrypt(enc_token, passphrase)

#     vk_api = VKAPIWrapper(dec_token)

#     try:
#         group_vk_id = CRUD.vk_group_methods.get_group_by_id(db, group_id).vk_id
#     except:
#         raise HTTPException(
#             status_code=500, detail=f"Group with ID {group_id} does not exist."
#         )

#     image_bytes = BytesIO(image.file.read())
#     logo_bytes = BytesIO(logo.file.read())
#     message = f"{title}%0A%0A{description}%0A%0A{source_url}"

#     generated_image = generate_image(
#         title=title,
#         description=description,
#         source=source,
#         image_bytes=image_bytes,
#         logo_bytes=logo_bytes,
#     )

#     generated_image.seek(0)

#     await vk_api.create_post(
#         group_id=group_vk_id,
#         message=message,
#         copyright=source_url,
#         image=generated_image,
#         image_filename="image.png",
#     )


@router.post("/vk_api/post")
async def post(
    auth: Annotated[bool, Depends(auth)],
    title: str = Form(),
    description: str = Form(),
    source: str = Form(),
    source_url: str = Form(),
    image: UploadFile = File(),
    usertoken_id: int = Form(),
    passphrase: str = Form(),
    group_id: int = Form(),
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
    message = f"{title}%0A%0A{description}%0A%0A{source_url}"

    await vk_api.create_post(
        group_id=group_vk_id,
        message=message,
        copyright=source_url,
        image=image_bytes,
        image_filename="image.png",
    )
