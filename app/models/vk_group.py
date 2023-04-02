"""VK group table model"""

from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class VKGroup(Base):
    __tablename__ = "vk_groups"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey("vk_usertokens.id"))

    token = relationship("VKUsertoken", back_populates="groups")