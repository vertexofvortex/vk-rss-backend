from pydantic import BaseModel


class RSSSourceLogoBase(BaseModel):
    source_id: int
    logo: bytes