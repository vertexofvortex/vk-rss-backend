from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.depends import get_db
from app.schemas.rss_post_schema import RSSPostBase, RSSPostCreate
from app.crud import CRUD


router = APIRouter()


@router.get("/posts", tags=["RSS posts"])
async def get_all_rss_posts(
    db: Session = Depends(get_db)
):
    return CRUD.rss_posts.get_all_posts(db)


@router.get("/posts/{post_id}", tags=["RSS posts"])
async def get_rss_posts_by_id(
    post_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_posts.get_post_by_id(db, post_id)


@router.get("/posts/by_source/{source_id}", tags=["RSS posts"])
async def get_rss_post_by_source_id(
    source_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_posts.get_posts_by_source_id(db, source_id)


@router.post("/posts", tags=["RSS posts"])
async def create_rss_post(
    post: RSSPostCreate,
    db: Session = Depends(get_db)
):
    return CRUD.rss_posts.create_post(db, post)


@router.put("/posts/{id}", tags=["RSS posts"])
async def update_rss_post(
    post: RSSPostBase,
    post_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_posts.update_post(db, post, post_id)


@router.delete("/posts/{id}", tags=["RSS posts"])
async def delete_rss_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_posts.delete_post(db, post_id)