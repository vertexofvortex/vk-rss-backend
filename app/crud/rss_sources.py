"""CRUD utils for RSS sources table"""

from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from app.models.rss_post import RSSPost
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

def update_source(db: Session, source_id: int, source: RSSSourceBase):
    upd_source = (
        update(RSSSource)
        .where(RSSSource.id == source_id)
        .values(**source.dict())
    )
    db.execute(upd_source)
    db.commit()

    return get_source_by_id(db, source_id)

def delete_source(db: Session, source_id: int):
    del_source = (
        delete(RSSSource)
        .where(RSSSource.id == source_id)
    )
    del_posts = (
        delete(RSSPost)
        .where(RSSPost.source_id == source_id)
    )
    db.execute(del_posts)
    db.execute(del_source)
    db.commit()

    return