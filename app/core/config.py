from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # 🗄 Database
    DATABASE_URL: str

    # 🔐 Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # ⏱ Tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    RESET_TOKEN_EXPIRE_MINUTES: int = 15

    #Seed Data
    RUN_SEED: bool = Field(default=False)

    # 📧 Email / SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str

    # 🌍 App
    FRONTEND_URL: str = Field(default="http://localhost:3000")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
