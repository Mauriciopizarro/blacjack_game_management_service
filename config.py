from pydantic import BaseSettings


class Settings(BaseSettings):
    GAME_SERVICE_URL: str
    DATABASE_MONGO_URL: str

    class Config:
        env_file = './.env'


settings = Settings()
