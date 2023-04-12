"""VK usertoken table model"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class VKUsertokenModel(Base):
    __tablename__ = "vk_usertokens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=False, unique=True)

    groups = relationship("VKGroupModel", back_populates="token")