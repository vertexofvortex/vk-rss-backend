"""API main entry point"""

from fastapi import FastAPI


api = FastAPI(title="VK RSS Bot API", version="0.1.0")

@api.get("/")
async def root():
    return "It works!"