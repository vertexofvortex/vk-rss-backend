"""VK usertoken pydantic schema"""

from pydantic import BaseModel

from app.schemas.vk_group_schema import VKGroup


class VKUsertokenBase(BaseModel):
    name: str
    token: str


class VKUsertokenCreate(VKUsertokenBase):
    passphrase: str


class VKUsertokenResponse(BaseModel):
    id: int
    name: str
    groups: list[VKGroup] = []

    class Config:
        orm_mode = True


class VKUsertoken(VKUsertokenBase):
    id: int
    groups: list[VKGroup] = []

    class Config:
        orm_mode = True