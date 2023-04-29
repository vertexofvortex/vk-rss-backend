from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1111"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_TABLE: str = "vk_rss_bot"
    JWT_SECRET_KEY: str = "themostsecretestsecretkeyyouhaveeverseeninyourlifeandiamnotgoingtochangethatbutformoresecurityiwilladdthisnumericcombinationtotheendofmysecretestjwtsecret1234"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    SERVICE_PASSWORD: str = "1563"
    BG_PARSING_INTERVAL_SECONDS: int = 900
    BG_CLEANUP_INTERVAL_SECONDS: int = 86400


settings = Settings()
