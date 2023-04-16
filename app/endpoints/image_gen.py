import base64
from io import BytesIO
from typing import Annotated
import aiohttp
from fastapi import APIRouter, File, Form, HTTPException, Response, UploadFile
from app.schemas.generated_image import GeneratedImageCreate

from app.utils.img_gen.img_gen import generate_image


router = APIRouter(tags=["Image generating"])


# @router.post("/check_image_gen")
# async def check_image_gen(
#     params: GeneratedImageCreate,
# ):
#     # try:
#     #     print("trying to fetch image...")
#     #     async with aiohttp.ClientSession() as session:
#     #         async with session.get(params.image) as response:
#     #             image_bytes = await response.read()
#     # except:
#     #     print("trying to decode base64...")
#     #     #print(params.image_url[0:30],"..." , params.image_url[len(params.image_url) - 30:len(params.image_url)])
#     #     base64.urlsafe_b64decode(params.image)
#     #     # print("fetching error")
#     #     # try:
#     #     #     print("trying to decode base64...")
#     #     #     print(params.image_url[0:30],"..." , params.image_url[len(params.image_url) - 30:len(params.image_url)])
#     #     #     base64.b64decode(params.image_url)
#     #     # except:
#     #     #     print("decoding error")
#     #     #     raise HTTPException(
#     #     #         status_code=500
#     #     #     )

#     # async with aiohttp.ClientSession() as session:
#     #     async with session.get(params.logo) as response:
#     #         logo_bytes = await response.read()

    

#     # generated_image = generate_image(
#     #     title=params.title,
#     #     description=params.description,
#     #     source=params.source,
#     #     image_bytes=BytesIO(image_bytes),
#     #     logo_bytes=BytesIO(image_bytes),
#     # )

#     # return Response(content=generated_image.getvalue(), media_type="image/png")

#     if type(params.image) is str:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(params.image) as response:
#                 image = await response.read()
#         print("image is url")
#     elif type(params.image) is bytes:
#         print("image is file")


@router.post("/check_image_gen")
async def check_image_gen(
    title: str = Form(),
    description: str = Form(),
    source: str = Form(),
    image: UploadFile = File(),
    logo: UploadFile = File(),
):
    generated_image = generate_image(
        title=title,
        description=description,
        source=source,
        image_bytes=BytesIO(image.file.read()),
        logo_bytes=BytesIO(logo.file.read()),
    )

    return Response(
        content=generated_image.getvalue(),
        media_type="image/png",
    )