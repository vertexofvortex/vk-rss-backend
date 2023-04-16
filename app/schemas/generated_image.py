from typing import Annotated, Union
from fastapi import File
from pydantic import BaseModel


class GeneratedImageCreate(BaseModel):
    title: str
    description: str
    source: str
    image: Union[str, Annotated[bytes, File()]]
    logo: Union[str, Annotated[bytes, File()]]