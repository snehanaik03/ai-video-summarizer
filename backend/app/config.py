from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    SECRET_KEY: str = "secret"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    UPLOAD_DIR: str = "./downloads"
    MAX_FILE_SIZE_MB: int = 500
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
