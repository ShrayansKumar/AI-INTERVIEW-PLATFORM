from typing import List, Optional
from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    filename: str
    cloudinary_url: str
    extracted_text_preview: str


class ProjectItem(BaseModel):
    name: str
    description: str


class ExperienceItem(BaseModel):
    role: str
    organization: str
    duration: Optional[str] = None


class EducationItem(BaseModel):
    institution: str
    degree: str
    cgpa_or_score: Optional[str] = None


class ExtracurricularItem(BaseModel):
    activity: str
    description: str


class StructuredResumeResponse(BaseModel):
    filename: str
    cloudinary_url: str
    extracted_text: str
    skills: List[str]
    projects: List[ProjectItem]
    experience: List[ExperienceItem]
    education: List[EducationItem]
    coursework: List[str] = []
    extracurriculars: List[ExtracurricularItem] = []


class ResumeRecordResponse(BaseModel):
    filename: str
    cloudinary_url: Optional[str]
    extracted_text: str
    structured_data: dict
    uploaded_at: str

    class Config:
        from_attributes = True