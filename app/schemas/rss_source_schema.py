"""RSS source pydantic schema"""

from typing import Union
from pydantic import BaseModel
from app.schemas.rss_post_schema import RSSPostModel


class RSSSourceBase(BaseModel):
    title: str
    description: str
    rss_url: str


class RSSSourceWithLogoCreate(RSSSourceBase):
    logo: Union[bytes, None]


class RSSSource(RSSSourceBase):
    id: int
    #posts: list[RSSPostModel] = []

    class Config:
        orm_mode = True