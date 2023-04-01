"""VK group table model"""

from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base


class VKGroup(Base):
    __tablename__ = "vk_groups"

    id = Column(Integer, primary_key=True, index=True)
    encrypted_token = Column(String, ForeignKey("vk_usertokens.encrypted_token"))