import uuid

from pydantic import BaseModel

class CompanyCreateRequest(BaseModel):
    name: str
    description: str | None = None


class CompanyResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None

    class Config:
        from_attributes = True



class KnowledgeChunkResponse(BaseModel):
    id: uuid.UUID
    content: str
    source: str | None
    company: str | None

    class Config:
        from_attributes = True

class KnowledgeChunkCreateRequest(BaseModel):
    content: str
    source: str
    company: str


class UserAdminResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str

    class Config:
        from_attributes = True

class RetrievalResponse(BaseModel):
    query: str
    company: str | None
    results: list[KnowledgeChunkResponse]

