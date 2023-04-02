"""VK usertoken table model"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class VKUsertoken(Base):
    __tablename__ = "vk_usertokens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=False, unique=True)

    groups = relationship("VKGroup", back_populates="token")