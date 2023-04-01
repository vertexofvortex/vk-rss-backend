from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.rss_sources import create_source, get_all_sources, get_source_by_id

from app.depends import get_db
from app.schemas.rss_source import RSSSourceBase


router = APIRouter()


@router.get("/sources", tags=["RSS sources"])
async def get_all_rss_sources(db: Session = Depends(get_db)):
    return get_all_sources(db)


@router.get("/sources/{id}", tags=["RSS sources"])
async def get_rss_source_by_id(id: int, db: Session = Depends(get_db)):
    return get_source_by_id(db, id)


@router.post("/sources", tags=["RSS sources"])
async def create_rss_source(source: RSSSourceBase, db: Session = Depends(get_db)):
    return create_source(db, source=source)


@router.put("/sources/{id}", tags=["RSS sources"])
async def update_rss_source():
    pass


@router.delete("/sources/{id}", tags=["RSS sources"])
async def delete_rss_source():
    pass