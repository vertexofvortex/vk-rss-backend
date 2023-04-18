from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class PasswordUtils:
    def hash_password():
        pass

    def verify_password():
        pass

    def create_access_token():
        pass

    def decode_access_token():
        pass


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer,
            self,
        ).__call__(request)
        exception = HTTPException(
            status_code=401,
        )

        if credentials:
            token = PasswordUtils.decode_access_token(credentials.credentials)

            if token is None:
                raise exception

            return credentials.credentials
        else:
            raise
