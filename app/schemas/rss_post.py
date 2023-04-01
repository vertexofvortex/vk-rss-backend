"""RSS post pydantic schema"""

from pydantic import BaseModel


class RSSPostBase(BaseModel):
    title: str
    description: str
    image_url: str
    post_url: str
    categories: str
    publish_date: str


class RSSPostCreate(RSSPostBase):
    source_id: int


class RSSPost(RSSPostBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True