"""CRUD utils for VK groups table"""

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.models.vk_group import VKGroup
from app.schemas.vk_group import VKGroupCreate


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