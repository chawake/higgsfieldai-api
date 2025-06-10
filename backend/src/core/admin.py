import jwt
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend

from src.core.config import settings


class AdminAuth(AuthenticationBackend):
    username = settings.ADMIN_USERNAME
    password = settings.ADMIN_PASSWORD

    @classmethod
    def _generate_token(cls) -> str:
        token = jwt.encode(payload={"sub": "admin"}, key=settings.SECRET_KEY, algorithm="HS256")
        return token

    @classmethod
    def _validate_token(cls, value: str | None) -> bool:
        if value is None:
            return False

        try:
            payload = jwt.decode(jwt=value, key=settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            return False

        return payload.get("sub") == "admin"

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username != self.username or password != self.password:
            return False

        request.session.update({"token": self._generate_token()})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return self._validate_token(token)


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
