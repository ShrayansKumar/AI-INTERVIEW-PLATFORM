import cloudinary
import cloudinary.uploader

from app.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def upload_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Uploads a resume PDF to Cloudinary and returns metadata.
    """
    result = cloudinary.uploader.upload(
        file_bytes,
        resource_type="auto",  # handles PDFs correctly
        folder="resumes",
        public_id=filename.rsplit(".", 1)[0],  # strip extension for the public_id
        overwrite=True,
    )
    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id"),
    }