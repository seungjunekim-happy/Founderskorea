from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Founderskorea"
    DATABASE_URL: str = "sqlite+aiosqlite:///./founderskorea.db"
    BASE_URL: str = "https://founderskorea.com"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
