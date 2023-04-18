from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.settings import settings


class PasswordUtils:
    def verify_password(password: str) -> bool:
        if password == settings.SERVICE_PASSWORD:
            return True
        else:
            return False

    def create_access_token(payload: dict) -> str | None:
        return jwt.encode(
            payload=payload, key=settings.JWT_SECRET_KEY, algorithm="HS256"
        )

    def decode_access_token(token: str):
        try:
            dec_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None

        return dec_token


# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(
#             JWTBearer,
#             self,
#         ).__call__(request)
#         print(credentials)
#         exception = HTTPException(
#             status_code=401,
#         )

#         if credentials:
#             token = PasswordUtils.decode_access_token(credentials.credentials)

#             if token is None:
#                 raise exception

#             return credentials.credentials
#         else:
#             raise


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        exp = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token"
        )
        if credentials:
            token = PasswordUtils.decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
