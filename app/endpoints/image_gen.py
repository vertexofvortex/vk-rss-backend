import base64
import traceback
from io import BytesIO
from typing import Annotated, Union

import aiohttp
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile

from app.schemas.generated_image import GeneratedImageCreate
from app.security import auth
from app.utils.img_gen.img_gen import generate_image

router = APIRouter(tags=["Image generating"])


@router.post("/generate_snippet")
async def generate_snippet(
    auth: Annotated[bool, Depends(auth)],
    title: str = Form(),
    description: str = Form(),
    source: str = Form(),
    image: Union[UploadFile, None] = File(None),
    image_url: Union[str, None] = Form(None),
    logo: UploadFile = File(),
):
    if (image) and (image_url is None):
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

    if (image_url is None) and (image is None):
        generated_image = generate_image(
            title=title,
            description=description,
            source=source,
            image_bytes=None,
            logo_bytes=BytesIO(logo.file.read()),
        )

        return Response(
            content=generated_image.getvalue(),
            media_type="image/png",
        )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                external_image = await response.read()

        generated_image = generate_image(
            title=title,
            description=description,
            source=source,
            image_bytes=BytesIO(external_image),
            logo_bytes=BytesIO(logo.file.read()),
        )

        return Response(
            content=generated_image.getvalue(),
            media_type="image/png",
        )
    except:
        raise HTTPException(
            status_code=500, detail="An error occured in image generation."
        )
