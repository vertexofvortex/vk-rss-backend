"""CRUD utils for RSS posts table"""

from sqlalchemy.orm import Session
from app.models.rss_post import RSSPost
from app.schemas.rss_post import RSSPostCreate


def get_all_posts(db: Session):
    return db.query(RSSPost).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(RSSPost).filter(RSSPost.id == post_id).first()

def get_posts_by_source_id(db: Session, source_id: int):
    return db.query(RSSPost).filter(RSSPost.source_id == source_id).all()

def create_post(db: Session, post: RSSPostCreate):
    db_post = RSSPost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post