"""VK group pydantic schema"""

from pydantic import BaseModel


class VKGroupBase(BaseModel):
    vk_id: int


class VKGroup(VKGroupBase):
    id: int
    token_id: int

    class Config:
        orm_mode = True