from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    BASE_URL: str = "http://localhost:8000"
    WHATSAPP_API_URL: str = ""
    WHATSAPP_API_TOKEN: str = ""
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # Cloudinary (image storage)
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_FOLDER: str = "quickturf"

    # SSLCommerz
    SSLCOMMERZ_STORE_ID: str
    SSLCOMMERZ_STORE_PASSWORD: str
    SSLCOMMERZ_IS_SANDBOX: bool = True
    SSLCOMMERZ_SUCCESS_URL: str
    SSLCOMMERZ_FAIL_URL: str
    SSLCOMMERZ_CANCEL_URL: str
    FRONTEND_URL: str

    # Vercel Cron protection
    CRON_SECRET: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
