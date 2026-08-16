import cloudinary
import cloudinary.uploader
import cloudinary.api

from app.config import settings


def configure_cloudinary():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


configure_cloudinary()


def upload_image(
    file_bytes: bytes,
    filename: str,
    content_type: str,
    folder: str = "turfs",
) -> str:
    """Upload an image to Cloudinary and return its secure URL."""
    resource_type = "image"
    public_id_suffix = filename.rsplit(".", 1)[0]

    result = cloudinary.uploader.upload(
        file_bytes,
        folder=f"{settings.CLOUDINARY_FOLDER}/{folder}",
        public_id=public_id_suffix,
        resource_type=resource_type,
    )

    return result.get("secure_url")
