from fastapi import APIRouter, Depends
from app.crud.rss_posts import create_posts
from app.crud.rss_sources import get_all_sources
from sqlalchemy.orm import Session
from app.depends import get_db

from app.utils.parser.parse import Parser


router = APIRouter(tags=["RSS parsing"])
parser = Parser()


@router.get("/parsing/force_parse")
async def force_parse(
    db: Session = Depends(get_db)
):
    sources = get_all_sources(db)
    posts = await parser.parse(sources)

    create_posts(db, posts)

    return posts