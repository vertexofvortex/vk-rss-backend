"""RSS post pydantic schema"""

from pydantic import BaseModel


class RSSPostBase(BaseModel):
    title: str | None
    description: str | None
    image_url: str | None
    post_url: str
    categories: str | None
    publish_date: int | None
    blacklisted: bool


class RSSPostCreate(RSSPostBase):
    source_id: int


class RSSPostModel(RSSPostBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True
