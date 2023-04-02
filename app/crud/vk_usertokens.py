"""CRUD utils for VK usertokens table"""

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from app.models.vk_group import VKGroup
from app.models.vk_usertoken import VKUsertoken
from app.schemas.vk_usertoken import VKUsertokenBase, VKUsertokenCreate
from app.utils.aes_tools.aes_cipher import aes_tools


def get_all_tokens(db: Session):
    return db.query(VKUsertoken).all()

def get_token_by_id(db: Session, usertoken_id: int):
    return db.query(VKUsertoken).filter(VKUsertoken.id == usertoken_id).first()

def create_token(db: Session, usertoken: VKUsertokenCreate):
    passphrase = usertoken.passphrase
    enc_token = aes_tools.encrypt(usertoken.token, passphrase)

    db_token = VKUsertoken(
        name=usertoken.name,
        token=enc_token
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token

def update_token(db: Session, usertoken_id: int, usertoken: VKUsertokenBase):
    upd_token = (
        update(VKUsertoken)
        .where(VKUsertoken.id == usertoken_id)
        .values(**usertoken.dict())
    )
    db.execute(upd_token)
    db.commit()

    return get_token_by_id(db, usertoken_id)

def delete_token(db: Session, usertoken_id: int):
    del_token = (
        delete(VKUsertoken)
        .where(VKUsertoken.id == usertoken_id)
    )
    del_groups = (
        delete(VKGroup)
        .where(VKGroup.token_id == usertoken_id)
    )
    db.execute(del_groups)
    db.execute(del_token)
    db.commit()

    return