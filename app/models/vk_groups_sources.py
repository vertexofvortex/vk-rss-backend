from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class VKGroupsSources(Base):
    __tablename__ = "vk_groups_sources"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("vk_groups.id"))
    source_id = Column(Integer, ForeignKey("rss_sources.id"))

    group = relationship("VKGroup", back_populates="sources")
    source = relationship("RSSSource", back_populates="groups")