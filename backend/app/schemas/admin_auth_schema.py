import uuid
from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminResponse(BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        from_attributes = True