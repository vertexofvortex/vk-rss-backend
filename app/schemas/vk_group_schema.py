"""VK group pydantic schema"""

from pydantic import BaseModel

from app.schemas.rss_post_schema import RSSPostModel


class VKGroupBase(BaseModel):
    vk_id: int
    name: str
    photo_url: str

class VKGroupCreate(VKGroupBase):
    token_id: int

class VKGroupRequest(BaseModel):
    vk_id: int
    token_id: int
    passphrase: str


class VKGroup(VKGroupBase):
    id: int
    token_id: int

    class Config:
        orm_mode = True


class VKGroupExternal(BaseModel):
    id: int
    name: str
    screen_name: str
    is_closed: int
    type: str
    is_admin: int
    admin_level: int
    is_member: int
    is_advertiser: int
    photo_50: str
    photo_100: str
    photo_200: str


class VKGroupWithPosts(VKGroup):
    posts: list[RSSPostModel]