import os
import uuid

from fastapi import UploadFile

from app.config import settings


def save_upload(file: UploadFile, subfolder: str = "turfs") -> str:
    folder_path = os.path.join(settings.UPLOAD_DIR, subfolder)
    os.makedirs(folder_path, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return f"{settings.BASE_URL}/{file_path}"
