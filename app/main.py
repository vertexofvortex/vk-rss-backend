"""API main entry point"""

from fastapi import FastAPI
from app.db.database import Base, engine
from app.endpoints import rss_sources
from app.endpoints import rss_posts


Base.metadata.create_all(engine)

api = FastAPI(title="VK RSS Bot API", version="0.1.0")


api.include_router(rss_sources.router)
api.include_router(rss_posts.router)


@api.get("/")
async def root():
    return "It works!"