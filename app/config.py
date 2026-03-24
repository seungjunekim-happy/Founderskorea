from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Founderskorea"
    DATABASE_URL: str = "sqlite+aiosqlite:///./founderskorea.db"
    BASE_URL: str = "https://founderskorea.com"
    ARTICLE_API_KEYS: str = "{}"  # JSON: {"key_name": "key_value"}

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
