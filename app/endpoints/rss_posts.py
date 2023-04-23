from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import CRUD
from app.depends import get_db
from app.schemas.rss_post_schema import RSSPostBase, RSSPostCreate
from app.security import auth

router = APIRouter(tags=["RSS posts"])


@router.get("/posts")
async def get_all_rss_posts(
    auth: Annotated[bool, Depends(auth)], db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.get_all_posts(db)


@router.get("/posts/{post_id}")
async def get_rss_posts_by_id(
    auth: Annotated[bool, Depends(auth)], post_id: int, db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.get_post_by_id(db, post_id)


@router.get("/posts/by_source/{source_id}")
async def get_rss_post_by_source_id(
    auth: Annotated[bool, Depends(auth)], source_id: int, db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.get_posts_by_source_id(db, source_id)


@router.post("/posts")
async def create_rss_post(
    auth: Annotated[bool, Depends(auth)],
    post: RSSPostCreate,
    db: Session = Depends(get_db),
):
    return CRUD.rss_posts_methods.create_post(db, post)


@router.put("/posts/{post_id}")
async def update_rss_post(
    auth: Annotated[bool, Depends(auth)],
    post: RSSPostBase,
    post_id: int,
    db: Session = Depends(get_db),
):
    return CRUD.rss_posts_methods.update_post(db, post, post_id)


@router.delete("/posts/{post_id}")
async def delete_rss_post(
    auth: Annotated[bool, Depends(auth)], post_id: int, db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.delete_post(db, post_id)


@router.get("/posts_blacklisted")
async def get_blacklisted_rss_posts(
    auth: Annotated[bool, Depends(auth)], db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.get_blacklisted_posts(db)


@router.put("/posts/{post_id}/block")
async def blacklist_rss_post(
    auth: Annotated[bool, Depends(auth)], post_id: int, db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.block_post(db, post_id)


@router.put("/posts/{post_id}/unblock")
async def unblacklist_rss_post(
    auth: Annotated[bool, Depends(auth)], post_id: int, db: Session = Depends(get_db)
):
    return CRUD.rss_posts_methods.unblock_post(db, post_id)
