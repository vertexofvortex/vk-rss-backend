"""RSS post pydantic schema"""

from pydantic import BaseModel


class RSSPostBase(BaseModel):
    title: str | None
    description: str | None
    image_url: str | None
    post_url: str
    categories: str | None
    publish_date: str | None


class RSSPostCreate(RSSPostBase):
    source_id: int


class RSSPost(RSSPostBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True