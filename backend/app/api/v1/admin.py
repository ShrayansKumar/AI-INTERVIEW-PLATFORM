import uuid

from fastapi import APIRouter, Depends, HTTPException
from app.tasks.health_check_task import health_check_task
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.admin import Admin
from app.schemas.company_schema import (
    CompanyCreateRequest,
    CompanyResponse,
    KnowledgeChunkCreateRequest,
    KnowledgeChunkResponse,
    UserAdminResponse,
)
from app.services.admin_service import (
    list_companies,
    create_company,
    delete_company,
    list_knowledge_chunks,
    create_knowledge_chunk,
    delete_knowledge_chunk,
    list_users,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


# ── Companies ────────────────────────────────────────────────────

@router.get("/companies", response_model=list[CompanyResponse])
async def get_companies(
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await list_companies(db)


@router.post("/companies", response_model=CompanyResponse, status_code=201)
async def add_company(
    payload: CompanyCreateRequest,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await create_company(db, payload.name, payload.description)


@router.delete("/companies/{company_id}", status_code=204)
async def remove_company(
    company_id: uuid.UUID,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    deleted = await delete_company(db, company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")


# ── Knowledge Base ───────────────────────────────────────────────

@router.get("/knowledge-base", response_model=list[KnowledgeChunkResponse])
async def get_knowledge_chunks(
    company: str | None = None,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await list_knowledge_chunks(db, company)


@router.post("/knowledge-base", response_model=KnowledgeChunkResponse, status_code=201)
async def add_knowledge_chunk(
    payload: KnowledgeChunkCreateRequest,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await create_knowledge_chunk(db, payload.content, payload.source, payload.company)


@router.delete("/knowledge-base/{chunk_id}", status_code=204)
async def remove_knowledge_chunk(
    chunk_id: uuid.UUID,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    deleted = await delete_knowledge_chunk(db, chunk_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Knowledge chunk not found")


# ── Users ─────────────────────────────────────────────────────────

@router.get("/users", response_model=list[UserAdminResponse])
async def get_users(
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await list_users(db)


# ── (Keep your Day 4 Celery test endpoints below if still present) ──


@router.post("/test-task")
async def trigger_test_task(name: str = "World"):
    task = health_check_task.delay(name)
    return {"task_id": task.id, "status": "queued"}


@router.get("/test-task/{task_id}")
async def check_test_task(task_id: str):
    task = health_check_task.AsyncResult(task_id)
    return {"task_id": task_id, "status": task.status, "result": task.result}