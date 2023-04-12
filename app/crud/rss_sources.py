"""CRUD utils for RSS sources table"""

from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from app.models.rss_post_model import RSSPostModel
from app.models.rss_source_model import RSSSourceModel
from app.schemas.rss_source_schema import RSSSourceBase


class RSSSourcesMethods:
    def __init__(self) -> None:
        pass


    def get_all_sources(self, db: Session):
        return db.query(RSSSourceModel).all()


    def get_source_by_id(self, db: Session, id: int):
        return db.query(RSSSourceModel).filter(RSSSourceModel.id == id).first()


    def create_source(self, db: Session, source: RSSSourceBase):
        db_source = RSSSourceModel(
            title=source.title,
            description=source.description,
            rss_url=source.rss_url
        )

        db.add(db_source)
        db.commit()
        db.refresh(db_source)

        return db_source


    def update_source(self, db: Session, source_id: int, source: RSSSourceBase):
        upd_source = (
            update(RSSSourceModel)
            .where(RSSSourceModel.id == source_id)
            .values(**source.dict())
        )
        db.execute(upd_source)
        db.commit()

        return self.get_source_by_id(db, source_id)


    def delete_source(self, db: Session, source_id: int):
        del_source = (
            delete(RSSSourceModel)
            .where(RSSSourceModel.id == source_id)
        )
        del_posts = (
            delete(RSSPostModel)
            .where(RSSPostModel.source_id == source_id)
        )
        db.execute(del_posts)
        db.execute(del_source)
        db.commit()

        return
    
rss_sources_methods = RSSSourcesMethods()