"""CRUD utils for RSS posts table"""

from sqlalchemy import select
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
        # get_post = (
        #     select(RSSPost)
        #     #.join(RSSSource, RSSPost.source_id == RSSSource.id)
        #     .where(RSSPost.id == post_id)
        # )
        
        # result = db.execute(get_post).first()
        # #print(dict(result))
        # return result._asdict()

        #return db.query(RSSPost).filter(RSSPost.id == post_id).first()

        return db.query(RSSPostModel).join(RSSSourceModel, RSSSourceModel.id == RSSPostModel.source_id).filter(RSSPostModel.id == post_id).first()


    def get_posts_by_source_id(self, db: Session, source_id: int):
        return db.query(RSSPostModel).filter(RSSPostModel.source_id == source_id).all()


    def create_post(self, db: Session, post: RSSPostCreate):
        db_post = RSSPostModel(**post.dict())

        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        return db_post


    # TODO: делать апдейт, а не скипать
    def create_posts(self, db: Session, posts: list[RSSPostCreate]):
        for post in posts:
            add_post = insert(RSSPostModel).values(**post.dict())
            add_post = add_post.on_conflict_do_nothing()
            
            db.execute(add_post)
            db.commit()

        return


    def update_post(self, db: Session, post: RSSPostBase, post_id: int):
        db.query(RSSPostModel).filter(RSSPostModel.id == post_id).update(values=post.dict())
        db.commit()


    def delete_post(self, db: Session, post_id: int):
        db.query(RSSPostModel).filter(RSSPostModel.id == post_id).delete()
        db.commit()


rss_posts_methods = RSSPostsMethods