"""CRUD utils for RSS posts table"""

import time

from httpx import delete
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.rss_post_model import RSSPostModel
from app.models.rss_source_model import RSSSourceModel
from app.schemas.rss_post_schema import RSSPostBase, RSSPostCreate
from app.settings import settings


class RSSPostsMethods:
    def __init__(self) -> None:
        pass

    def get_all_posts(self, db: Session):
        return (
            db.query(RSSPostModel)
            .filter(RSSPostModel.blacklisted != True)
            .order_by(-RSSPostModel.publish_date)
            .all()
        )

    def get_post_by_id(self, db: Session, post_id: int):
        result = (
            db.execute(select(RSSPostModel).where(RSSPostModel.id == post_id))
            .scalars()
            .first()
        )

        return result

    def get_posts_by_source_id(self, db: Session, source_id: int):
        return db.query(RSSPostModel).filter(RSSPostModel.source_id == source_id).all()

    def create_post(self, db: Session, post: RSSPostCreate):
        db_post = RSSPostModel(**post.dict())

        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        return db_post

    def create_posts(self, db: Session, posts: list[RSSPostCreate]):
        for post in posts:
            add_post = (
                insert(RSSPostModel).values(**post.dict()).on_conflict_do_nothing()
            )

            db.execute(add_post)

        db.commit()

        return

    def update_post(self, db: Session, post: RSSPostBase, post_id: int):
        db.query(RSSPostModel).filter(RSSPostModel.id == post_id).update(
            values=post.dict()
        )
        db.commit()

    def delete_post(self, db: Session, post_id: int):
        db.query(RSSPostModel).filter(RSSPostModel.id == post_id).delete()
        db.commit()

    def block_post(self, db: Session, post_id: int):
        db.query(RSSPostModel).filter(RSSPostModel.id == post_id).update(
            values={"blacklisted": True}
        )
        db.commit()

    def unblock_post(self, db: Session, post_id: int):
        db.query(RSSPostModel).filter(RSSPostModel.id == post_id).update(
            values={"blacklisted": False}
        )
        db.commit()

    def get_blacklisted_posts(self, db: Session):
        return db.query(RSSPostModel).filter(RSSPostModel.blacklisted == True).all()

    def clear_old_posts(self, db: Session):
        db.query(RSSPostModel).filter(
            RSSPostModel.publish_date
            < int(time.time()) - settings.BG_CLEANUP_INTERVAL_SECONDS
        ).delete()
        db.commit()

        posts = db.query(RSSPostModel).all()

        return len(posts)


rss_posts_methods = RSSPostsMethods()
