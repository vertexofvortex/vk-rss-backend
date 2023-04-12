from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import CRUD
from app.depends import get_db
from app.schemas.rss_source_schema import RSSSourceBase
from app.utils.parser.parse import Parser


router = APIRouter(tags=["RSS sources"])
parser = Parser()


@router.get("/sources/check")
async def check_source_url(
    url: str,
    db: Session = Depends(get_db)
):
    check_results = await parser.checkFeed(url)

    if check_results:
        return check_results
    else:
        raise HTTPException(detail="URL is not found", status_code=404)


@router.get("/sources")
async def get_all_rss_sources(
    db: Session = Depends(get_db)
):
    return CRUD.rss_sources_methods.get_all_sources(db)


@router.get("/sources/{source_id}")
async def get_rss_source_by_id(
    source_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_sources_methods.get_source_by_id(db, id)


@router.post("/sources")
async def create_rss_source(
    source: RSSSourceBase,
    db: Session = Depends(get_db)
):
    return CRUD.rss_sources_methods.create_source(db, source=source)


@router.put("/sources/{source_id}")
async def update_rss_source(
    source_id: int,
    source: RSSSourceBase,
    db: Session = Depends(get_db)
):
    return CRUD.rss_sources_methods.update_source(db, source_id, source)


@router.delete("/sources/{source_id}")
async def delete_rss_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_sources_methods.delete_source(db, source_id)