from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.config import settings

ADMIN_TOKEN_EXPIRE_MINUTES = 60


def create_admin_token(admin_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ADMIN_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": admin_id, "exp": expire, "type": "admin_access"}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_admin_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if payload.get("type") != "admin_access":
            return None
        return payload
    except JWTError:
        return None