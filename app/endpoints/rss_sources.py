from typing import List, Optional, Union
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session
from app.crud import CRUD
from app.depends import get_db
from app.schemas.rss_source_schema import RSSSource, RSSSourceBase, RSSSourceWithLogoCreate
from app.utils.parser.parse import Parser


router = APIRouter(tags=["RSS sources"])
parser = Parser()


@router.get("/sources/check")
async def check_source_url(
    url: str,
):
    check_results = await parser.checkFeed(url)

    if check_results:
        return check_results
    else:
        raise HTTPException(detail="URL is not found", status_code=404)


@router.get("/sources")
async def get_all_rss_sources(
    db: Session = Depends(get_db)
) -> List[RSSSource]:
    return CRUD.rss_sources_methods.get_all_sources(db)


@router.get("/sources/{source_id}")
async def get_rss_source_by_id(
    source_id: int,
    db: Session = Depends(get_db)
):
    result = CRUD.rss_sources_methods.get_source_by_id(db, source_id)

    return result


@router.get("/source_logo/{source_id}")
async def get_rss_source_logo(
    source_id: int,
    db: Session = Depends(get_db),
):
    logo = CRUD.rss_sources_methods.get_source_logo(db, source_id)

    return Response(
        content=logo,
        media_type="image/png",
    )


@router.post("/sources")
async def create_rss_source(
    title: str = Form(),
    description: Optional[str] = Form(""),
    rss_url: str = Form(),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if logo is not None:
        return CRUD.rss_sources_methods.create_source(
            db,
            RSSSourceWithLogoCreate(
                title=title,
                description=description,
                rss_url=rss_url,
                logo=logo.file.read(),
            )
        )
    else:
        return CRUD.rss_sources_methods.create_source(
            db,
            RSSSourceBase(
                title=title,
                description=description,
                rss_url=rss_url,
            )
    )

@router.put("/sources/{source_id}")
async def update_rss_source(
    source_id: int,
    title: str = Form(),
    description: str = Form(),
    rss_url: str = Form(),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if logo:
        return CRUD.rss_sources_methods.create_source(
            db,
            source_id,
            RSSSourceWithLogoCreate(
                title=title,
                description=description,
                rss_url=rss_url,
                logo=logo.file.read().hex(),
            )
        )
    else:
        return CRUD.rss_sources_methods.update_source(
            db,
            source_id,
            RSSSourceBase(
                title=title,
                description=description,
                rss_url=rss_url,
            )
        )


@router.delete("/sources/{source_id}")
async def delete_rss_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    return CRUD.rss_sources_methods.delete_source(db, source_id)