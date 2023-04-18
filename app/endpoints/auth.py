from datetime import timedelta
import time
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.security import create_access_token, verify_password
from app.settings import settings


router = APIRouter(tags=["Authorization"])


@router.post("/auth/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not verify_password(form_data.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"test": True},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
