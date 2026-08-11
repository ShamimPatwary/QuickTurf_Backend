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


    SSLCOMMERZ_STORE_ID: str
    SSLCOMMERZ_STORE_PASSWORD: str
    SSLCOMMERZ_IS_SANDBOX: bool = True
    SSLCOMMERZ_SUCCESS_URL: str 
    SSLCOMMERZ_FAIL_URL: str
    SSLCOMMERZ_CANCEL_URL: str
    FRONTEND_URL: str



    class Config:
        env_file = ".env"


settings = Settings()
