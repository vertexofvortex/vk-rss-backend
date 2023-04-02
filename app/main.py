"""API main entry point"""

from fastapi import FastAPI
from app.db.database import Base, engine
from app.endpoints import rss_sources, rss_posts, vk_usertokens


Base.metadata.create_all(engine)

api = FastAPI(title="VK RSS Bot API", version="0.1.0")


api.include_router(rss_sources.router)
api.include_router(rss_posts.router)
api.include_router(vk_usertokens.router)


@api.get("/")
async def root():
    return "It works!"