from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    UPLOAD_DIR: str = "uploads"
    BASE_URL: str = "http://localhost:8000"
    WHATSAPP_API_URL: str = ""
    WHATSAPP_API_TOKEN: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
