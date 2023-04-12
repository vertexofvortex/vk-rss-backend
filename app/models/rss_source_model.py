"""RSS source model"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class RSSSourceModel(Base):
    __tablename__ = "rss_sources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    rss_url = Column(String, nullable=False)
    
    posts = relationship("RSSPostModel", back_populates="source")
    groups = relationship("VKGroupSourceModel", back_populates="source")