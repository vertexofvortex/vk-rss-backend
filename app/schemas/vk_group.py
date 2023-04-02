"""VK group pydantic schema"""

from pydantic import BaseModel


class VKGroupBase(BaseModel):
    vk_id: int


class VKGroupCreate(VKGroupBase):
    token_id: int


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
