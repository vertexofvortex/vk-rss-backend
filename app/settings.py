from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1111"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_TABLE: str = "vk_rss_bot_empty"


settings = Settings()
