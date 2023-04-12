from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship

def generateDefault(context):
    group_id = context.get_current_parameters()["group_id"]
    source_id = context.get_current_parameters()["source_id"]

    return f"{group_id}:{source_id}"


class VKGroupSourceModel(Base):
    __tablename__ = "vk_groups_sources"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("vk_groups.id"))
    source_id = Column(Integer, ForeignKey("rss_sources.id"))
    identity = Column(String, unique=True, default=generateDefault)

    group = relationship("VKGroupModel", back_populates="sources")
    source = relationship("RSSSourceModel", back_populates="groups")