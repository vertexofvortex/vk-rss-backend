"""CRUD utils for VK groups table"""

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from app.models.rss_source import RSSSource

from app.models.vk_group import VKGroup
from app.models.vk_groups_sources import VKGroupsSources
from app.schemas.vk_group import VKGroupCreate
from app.schemas.vk_groups_sources import VKGroupSourceBase


def get_all_groups(db: Session):
    return db.query(VKGroup).all()

def get_group_by_id(db: Session, group_id: int):
    return db.query(VKGroup).filter(VKGroup.id == group_id).first()

def get_groups_by_token_id(db: Session, token_id):
    return db.query(VKGroup).filter(VKGroup.token_id == token_id).all()

def create_group(db: Session, group: VKGroupCreate):
    db_group = VKGroup(**group.dict())

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group

def update_group(db: Session, group_id: int, group: VKGroupCreate):
    upd_group = (
        update(VKGroup)
        .where(VKGroup.id == group_id)
        .values(**group.dict())
    )

    db.execute(upd_group)
    db.commit

    return get_group_by_id(db, group_id)

def delete_group(db: Session, group_id: int):
    del_group = (
        delete(VKGroup)
        .where(VKGroup.id == group_id)
    )
    
    db.execute(del_group)
    db.commit()

    return


# extras

def get_group_sources(db: Session, group_id: int):
    group_sources = db.query(VKGroupsSources).filter(VKGroupsSources.group_id == group_id).all()
    result = []

    for source in group_sources:
        result.append(db.query(RSSSource).filter(RSSSource.id == source.source_id).one())

    return result

def create_group_source(db: Session, group_source: VKGroupSourceBase):
    # add_source = (
    #     insert(VKGroupsSources)
    #     .values(**group_source.dict())
    # )

    db.add(VKGroupsSources(**group_source.dict()))
    # db.execute(add_source)
    db.commit()

    return