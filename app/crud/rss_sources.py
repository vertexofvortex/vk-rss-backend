"""CRUD utils for RSS sources table"""

from typing import List
from sqlalchemy import delete, insert, update
from sqlalchemy.orm import Session
from app.models.rss_post_model import RSSPostModel
from app.models.rss_source_logo import RSSSourceLogo
from app.models.rss_source_model import RSSSourceModel
from app.models.vk_group_source_model import VKGroupSourceModel
from app.schemas.rss_source_logo_schema import RSSSourceLogoBase
from app.schemas.rss_source_schema import RSSSourceBase, RSSSourceWithLogoCreate
from app.schemas.vk_group_source_schema import VKGroupSource


class RSSSourcesMethods:
    def __init__(self) -> None:
        pass

    def get_all_sources(self, db: Session):
        result = db.query(RSSSourceModel).all()

        return result

    def get_source_by_id(self, db: Session, id: int):
        return db.query(RSSSourceModel).filter(RSSSourceModel.id == id).first()

    def create_source(
        self, db: Session, source: RSSSourceBase | RSSSourceWithLogoCreate
    ):
        db_source = RSSSourceModel(
            title=source.title, description=source.description, rss_url=source.rss_url
        )

        db.add(db_source)
        db.commit()
        db.refresh(db_source)

        if hasattr(source, "logo"):
            db_logo = RSSSourceLogo(source_id=db_source.id, logo=source.logo)

            db.add(db_logo)
            db.commit()

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
        del_source = delete(RSSSourceModel).where(RSSSourceModel.id == source_id)
        del_posts = delete(RSSPostModel).where(RSSPostModel.source_id == source_id)
        del_logo = delete(RSSSourceLogo).where(RSSSourceLogo.source_id == source_id)
        del_group_sources = delete(VKGroupSourceModel).where(
            VKGroupSourceModel.source_id == source_id
        )
        db.execute(del_posts)
        db.execute(del_logo)
        db.execute(del_group_sources)
        db.execute(del_source)
        db.commit()

        return

    def get_source_logo(self, db: Session, source_id: int):
        result = (
            db.query(RSSSourceLogo).filter(RSSSourceLogo.source_id == source_id).first()
        )

        return result.logo


rss_sources_methods = RSSSourcesMethods()
