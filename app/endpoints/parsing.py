from typing import Annotated
from fastapi import APIRouter, Depends
from app.crud import CRUD
from sqlalchemy.orm import Session
from app.depends import get_db
from app.security import auth

from app.utils.parser.parser import Parser


router = APIRouter(tags=["RSS parsing"])
parser = Parser()


@router.get("/parsing/force_parse")
async def force_parse(
    auth: Annotated[bool, Depends(auth)], db: Session = Depends(get_db)
):
    sources = CRUD.rss_sources_methods.get_all_sources(db)
    posts = await parser.parse(sources)

    CRUD.rss_posts_methods.create_posts(db, posts)

    return len(posts)
