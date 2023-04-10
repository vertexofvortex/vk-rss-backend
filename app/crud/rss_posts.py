"""CRUD utils for RSS posts table"""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.models.rss_post import RSSPost
from app.schemas.rss_post import RSSPostBase, RSSPostCreate
from app.crud.rss_sources import get_source_by_id
from app.models.rss_source import RSSSource


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

# TODO: делать апдейт, а не скипать
def create_posts(db: Session, posts: list[RSSPostCreate]):
    for post in posts:
        add_post = insert(RSSPost).values(**post.dict())
        add_post = add_post.on_conflict_do_nothing()
        
        db.execute(add_post)
        db.commit()

    return

def update_post(db: Session, post: RSSPostBase, post_id: int):
    db.query(RSSPost).filter(RSSPost.id == post_id).update(values=post.dict())
    db.commit()

def delete_post(db: Session, post_id: int):
    db.query(RSSPost).filter(RSSPost.id == post_id).delete()
    db.commit()