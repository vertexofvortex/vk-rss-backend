"""RSS post model"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class RSSPostModel(Base):
    __tablename__ = "rss_posts"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("rss_sources.id"))
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    post_url = Column(String, nullable=False, unique=True)
    categories = Column(String, nullable=True)
    # TODO: publish_date must be a DateTime
    publish_date = Column(Integer, nullable=True)

    source = relationship("RSSSourceModel", back_populates="posts")
