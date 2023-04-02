"""VK usertoken pydantic schema"""

from pydantic import BaseModel

from app.schemas.vk_group import VKGroup


class VKUsertokenBase(BaseModel):
    name: str
    token: str


class VKUsertoken(VKUsertokenBase):
    id: int
    groups: list[VKGroup] = []

    class Config:
        orm_mode = True