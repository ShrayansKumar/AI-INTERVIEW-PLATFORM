from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.resume_schema import StructuredResumeResponse, ResumeRecordResponse
from app.services.resume_parser_service import extract_text_from_pdf, structure_resume_text
from app.utils.file_storage import upload_resume
from app.services.resume_storage_service import get_user_resume, save_user_resume
from app.services.resume_chunking_service import embed_and_store_resume_chunks

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])


@router.post("/upload", response_model=StructuredResumeResponse)
async def upload_resume_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)

    if not extracted_text:
        raise HTTPException(status_code=400, detail="Could not extract any text from this PDF")

    try:
        structured_data = structure_resume_text(extracted_text)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Failed to structure resume via LLM: {str(e)}")

    upload_result = upload_resume(file_bytes, file.filename)

    # Persist parsed resume to DB so it doesn't need re-uploading every time
    await save_user_resume(
        db,
        user_id=current_user.id,
        filename=file.filename,
        cloudinary_url=upload_result["url"],
        extracted_text=extracted_text,
        structured_data=structured_data,
    )

    # Chunk + embed the resume into resume_chunks, so question_agent can RAG-retrieve from it
    await embed_and_store_resume_chunks(db, current_user.id, structured_data, extracted_text)

    return StructuredResumeResponse(
        filename=file.filename,
        cloudinary_url=upload_result["url"],
        extracted_text=extracted_text,
        skills=structured_data.get("skills", []),
        projects=structured_data.get("projects", []),
        experience=structured_data.get("experience", []),
        education=structured_data.get("education", []),
        coursework=structured_data.get("coursework", []),
        extracurriculars=structured_data.get("extracurriculars", []),
    )


@router.get("/current", response_model=ResumeRecordResponse | None)
async def get_current_resume(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns the user's previously uploaded resume, if one exists.
    Frontend calls this on app load to skip re-upload if already on file.
    """
    resume = await get_user_resume(db, current_user.id)
    if not resume:
        return None

    return ResumeRecordResponse(
        filename=resume.filename,
        cloudinary_url=resume.cloudinary_url,
        extracted_text=resume.extracted_text,
        structured_data=resume.structured_data,
        uploaded_at=resume.uploaded_at.isoformat(),
    )