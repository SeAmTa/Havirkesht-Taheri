from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "havirkesht"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""

    # 1 یعنی فعلاً قفل (Auth) خاموش، 0 یعنی روشن
    DISABLE_AUTH: int = 1

    # JWT
    JWT_SECRET: str = "change-this-secret"
    JWT_REFRESH_SECRET: str = "change-this-refresh-secret"
    JWT_ALG: str = "HS256"

    # زمان انقضا
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def database_url(self) -> str:
        pwd = quote_plus(self.DB_PASSWORD or "")
        user = quote_plus(self.DB_USER or "")
        return (
            f"mysql+pymysql://{user}:{pwd}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    class Config:
        env_file = ".env"


settings = Settings()
