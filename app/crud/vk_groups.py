"""CRUD utils for VK groups table"""

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from app.crud.rss_posts import get_posts_by_source_id
from app.crud.vk_usertokens import get_token_by_id
from app.models.rss_source import RSSSource

from app.models.vk_group import VKGroup
from app.models.vk_groups_sources import VKGroupsSources
from app.schemas.rss_post import RSSPost
from app.schemas.vk_group import VKGroupCreate, VKGroupRequest, VKGroupWithPosts
from app.schemas.vk_groups_sources import VKGroupSourceBase
from app.utils.aes_tools.aes_cipher import AESTools
from app.utils.vk_api_wrapper.vk_api_wrapper import VKAPIWrapper


class VKGroupMethods:
    def __init__(self) -> None:
        pass


    def get_all_groups(
        self,
        db: Session,
    ):
        get_groups = (
            select(VKGroup)
        )

        #return db.execute(get_groups).all()
        return db.query(VKGroup).all()
    

    def get_group_by_id(
        self,
        db: Session,
        group_id: int,
    ):
        get_group = (
            select(VKGroup)
            .where(VKGroup.id == group_id)
        )

        return db.execute(get_group).first()
    

    def get_groups_by_token_id(
        self,
        db: Session, 
        token_id: int,
        passphrase: str,
    ):
        # TODO:
        pass

    async def create_group(
        self,
        db: Session,
        group: VKGroupRequest,
    ):
        aes_tools = AESTools()
        enc_token = get_token_by_id(db, group.token_id).token
        dec_token = aes_tools.decrypt(enc_token, group.passphrase)
        
        vk_api = VKAPIWrapper(dec_token)

        try:
            vk_group = await vk_api.get_group_by_id(group.vk_id)
        except:
            raise # TODO: чё raisим?

        db_group = VKGroupCreate(
            vk_id=vk_group.id,
            name=vk_group.name,
            photo_url=vk_group.photo_200,
            token_id=group.token_id,
        )

        add_group = (
            insert(VKGroup)
            .values(**db_group.dict())
        )

        db.execute(add_group)
        db.commit()
        
        return


    def update_group(
        self,
        db: Session,
        group_id: int,
        group: VKGroupCreate,
    ):
        # TODO:
        pass


    def delete_group(
        self,
        db: Session,
        group_id: int,
    ):
        # TODO:
        pass


    def get_group_posts(
        self,
        db: Session,
        group_id: int,
    ):
        group = get_group_by_id(db, group_id)
        group_sources = get_group_sources(db, group_id)
        posts = []

        for source in group_sources:
            posts += get_posts_by_source_id(db, source.id)

        return VKGroupWithPosts(
            id=group.id,
            name=group.name,
            photo_url=group.photo_url,
            token_id=group.token_id,
            vk_id=group.vk_id,
            posts=posts,
        )
    

    def get_all_groups_posts(
        self,
        db: Session,
    ):
        groups = get_all_groups(db)
        groups_with_posts = []

        for group in groups:
            groups_with_posts.append(self.get_group_posts(db, group.id))

        return groups_with_posts


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