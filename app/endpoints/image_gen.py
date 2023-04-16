import base64
from io import BytesIO
from typing import Annotated
import aiohttp
from fastapi import APIRouter, File, Form, HTTPException, Response, UploadFile
from app.schemas.generated_image import GeneratedImageCreate

from app.utils.img_gen.img_gen import generate_image


router = APIRouter(tags=["Image generating"])


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