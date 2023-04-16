from sqlalchemy import Column, ForeignKey, Integer, LargeBinary
from app.db.database import Base



class RSSSourceLogo(Base):
    __tablename__ = "rss_sources_logos"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("rss_sources.id"))
    logo = Column(LargeBinary, nullable=True)