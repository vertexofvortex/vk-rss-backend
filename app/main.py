"""API main entry point"""

from pathlib import Path
from fastapi import Depends, FastAPI
import uvicorn
from app.crud import CRUD
from app.db.database import Base, engine
from app.depends import get_db
from app.endpoints import (
    rss_sources,
    rss_posts,
    vk_usertokens,
    vk_groups,
    vk_api,
    parsing,
    image_gen,
    auth,
)
from fastapi.middleware.cors import CORSMiddleware
from app.utils.parser.parser import Parser
from app.utils.parser.parsing_daemon import ParsingDaemon
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)
api = FastAPI(title="VK RSS Bot API", version="0.1.0")
parsing_daemon = ParsingDaemon()


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api.include_router(rss_sources.router)
api.include_router(rss_posts.router)
api.include_router(vk_usertokens.router)
api.include_router(vk_groups.router)
api.include_router(vk_api.router)
api.include_router(parsing.router)
api.include_router(image_gen.router)
api.include_router(auth.router)


@api.get("/")
async def root(db: Session = Depends(get_db)):
    return "Hi"


@api.on_event("startup")
async def startup():
    parsing_daemon.start()
