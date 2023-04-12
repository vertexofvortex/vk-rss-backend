"""CRUD utils for VK groups table"""

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.crud.vk_usertokens import vk_usertoken_methods
from app.models.rss_source_model import RSSSourceModel
from app.crud import rss_posts
from app.models.vk_group_model import VKGroupModel
from app.models.vk_group_source_model import VKGroupSourceModel
from app.schemas.rss_post_schema import RSSPostModel
from app.schemas.vk_group_schema import VKGroupCreate, VKGroupRequest, VKGroupWithPosts
from app.schemas.vk_group_source_schema import VKGroupSourceBase
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
            select(VKGroupModel)
        )

        #return db.execute(get_groups).all()
        return db.query(VKGroupModel).all()
    

    def get_group_by_id(
        self,
        db: Session,
        group_id: int,
    ):
        get_group = (
            select(VKGroupModel)
            .where(VKGroupModel.id == group_id)
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
        enc_token = vk_usertoken_methods.get_token_by_id(db, group.token_id).token
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
            insert(VKGroupModel)
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
            posts += rss_posts.get_posts_by_source_id(db, source.id)

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
    

    def create_group_sources(
        self,
        db: Session,
        group_sources: list[VKGroupSourceBase],
    ):
        for source in group_sources:
            #db.add(VKGroupsSources(**source.dict()))
            db.execute(
                insert(VKGroupSourceModel)
                .values(**source.dict())
                .on_conflict_do_nothing()
            )

        db.commit()
    

    def delete_group_source(
        self,
        db: Session,
        group_id: int,
        source_id: int,
    ):
        del_source = (
            delete(VKGroupSourceModel)
            .where(
                VKGroupSourceModel.source_id == source_id,
                VKGroupSourceModel.group_id == group_id
            )
        )
        db.execute(del_source)
        db.commit()

        return get_group_sources(db, group_id)
    


def get_all_groups(db: Session):
    return db.query(VKGroupModel).all()

def get_group_by_id(db: Session, group_id: int):
    return db.query(VKGroupModel).filter(VKGroupModel.id == group_id).first()

def get_groups_by_token_id(db: Session, token_id):
    return db.query(VKGroupModel).filter(VKGroupModel.token_id == token_id).all()

def create_group(db: Session, group: VKGroupCreate):
    db_group = VKGroupModel(**group.dict())

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group

def update_group(db: Session, group_id: int, group: VKGroupCreate):
    upd_group = (
        update(VKGroupModel)
        .where(VKGroupModel.id == group_id)
        .values(**group.dict())
    )

    db.execute(upd_group)
    db.commit

    return get_group_by_id(db, group_id)

def delete_group(db: Session, group_id: int):
    del_group = (
        delete(VKGroupModel)
        .where(VKGroupModel.id == group_id)
    )
    del_group_sources = (
        delete(VKGroupSourceModel)
        .where(VKGroupSourceModel.group_id == group_id)
    )
    
    db.execute(del_group_sources)
    db.execute(del_group)
    db.commit()

    return


# extras

def get_group_sources(db: Session, group_id: int):
    group_sources = db.query(VKGroupSourceModel).filter(VKGroupSourceModel.group_id == group_id).all()
    result = []

    for source in group_sources:
        result.append(db.query(RSSSourceModel).filter(RSSSourceModel.id == source.source_id).one())

    return result

def create_group_source(db: Session, group_source: VKGroupSourceBase):
    # add_source = (
    #     insert(VKGroupsSources)
    #     .values(**group_source.dict())
    # )

    db.add(VKGroupSourceModel(**group_source.dict()))
    # db.execute(add_source)
    db.commit()

    return


vk_group_methods = VKGroupMethods()