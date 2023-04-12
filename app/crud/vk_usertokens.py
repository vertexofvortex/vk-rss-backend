"""CRUD utils for VK usertokens table"""

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from app.models.vk_group_model import VKGroupModel
from app.models.vk_usertoken_model import VKUsertokenModel
from app.schemas.vk_usertoken_schema import VKUsertokenBase, VKUsertokenCreate
from app.utils.aes_tools.aes_cipher import aes_tools


class VKUsertokensMethods:
    def get_all_tokens(self, db: Session):
        return db.query(VKUsertokenModel).all()


    def get_token_by_id(self, db: Session, usertoken_id: int):
        return db.query(VKUsertokenModel).filter(VKUsertokenModel.id == usertoken_id).first()


    def create_token(db: Session, usertoken: VKUsertokenCreate):
        enc_token = aes_tools.encrypt(usertoken.token, usertoken.passphrase)
        print(enc_token)
        dec_token = aes_tools.decrypt(enc_token, usertoken.passphrase)
        print(dec_token)

        add_token = (
            insert(VKUsertokenModel)
            .values({
                "name": usertoken.name,
                "token": enc_token,
            })
        )

        db.execute(add_token)
        db.commit()

        return


    def update_token(self, db: Session, usertoken_id: int, usertoken: VKUsertokenBase):
        upd_token = (
            update(VKUsertokenModel)
            .where(VKUsertokenModel.id == usertoken_id)
            .values(**usertoken.dict())
        )
        db.execute(upd_token)
        db.commit()

        return self.get_token_by_id(db, usertoken_id)


    def delete_token(self, db: Session, usertoken_id: int):
        del_token = (
            delete(VKUsertokenModel)
            .where(VKUsertokenModel.id == usertoken_id)
        )
        del_groups = (
            delete(VKGroupModel)
            .where(VKGroupModel.token_id == usertoken_id)
        )
        db.execute(del_groups)
        db.execute(del_token)
        db.commit()

        return
    

vk_usertoken_methods = VKUsertokensMethods()