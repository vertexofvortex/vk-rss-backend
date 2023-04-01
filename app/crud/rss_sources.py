"""CRUD utils for RSS sources table"""

from sqlalchemy.orm import Session
from app.models.rss_source import RSSSource
from app.schemas.rss_source import RSSSourceBase


def get_all_sources(db: Session):
    return db.query(RSSSource).all()

def get_source_by_id(db: Session, id: int):
    return db.query(RSSSource).filter(RSSSource.id == id).first()

def create_source(db: Session, source: RSSSourceBase):
    db_source = RSSSource(
        title=source.title,
        description=source.description,
        rss_url=source.rss_url
    )

    db.add(db_source)
    db.commit()
    db.refresh(db_source)

    return db_source

def update_source(db: Session, id: int):
    pass

def delete_source(db: Session, id: int):
    pass