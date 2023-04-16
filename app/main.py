"""API main entry point"""

from pathlib import Path
from fastapi import FastAPI
from app.db.database import Base, engine
from app.endpoints import rss_sources, rss_posts, vk_usertokens, vk_groups, vk_api, parsing, image_gen
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(engine)


api = FastAPI(title="VK RSS Bot API", version="0.1.0")


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


@api.get("/")
async def root():
    return "It works!"