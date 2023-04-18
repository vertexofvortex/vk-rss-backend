from fastapi import Depends, HTTPException
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def auth(token: str = Depends(JWTBearer())):
#     print(token)
#     payload = PasswordUtils.decode_access_token(token)
#     credentials_exception = HTTPException(status_code=401)

#     if payload is None:
#         raise credentials_exception

#     return True
