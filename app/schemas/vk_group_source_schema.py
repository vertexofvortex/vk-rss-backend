from pydantic import BaseModel


class VKGroupSourceBase(BaseModel):
    group_id: int
    source_id: int


class VKGroupSource(VKGroupSourceBase):
    id: int

    class Config:
        orm_mode = True