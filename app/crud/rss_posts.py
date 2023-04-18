"""CRUD utils for RSS posts table"""

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.models.rss_post_model import RSSPostModel
from app.schemas.rss_post_schema import RSSPostBase, RSSPostCreate
from app.models.rss_source_model import RSSSourceModel


class RSSPostsMethods:
    def __init__(self) -> None:
        pass

    def get_all_posts(self, db: Session):
        return db.query(RSSPostModel).all()

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


rss_posts_methods = RSSPostsMethods()
