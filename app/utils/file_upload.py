import uuid

from fastapi import UploadFile

from app.services.storage import upload_image


def save_upload(file: UploadFile, subfolder: str = "turfs") -> str:
    """Upload a file to Cloudinary and return its public URL."""
    file_bytes = file.file.read()
    filename = file.filename or f"{uuid.uuid4().hex}.png"
    content_type = file.content_type or "image/*"

    return upload_image(
        file_bytes=file_bytes,
        filename=filename,
        content_type=content_type,
        folder=subfolder,
    )
