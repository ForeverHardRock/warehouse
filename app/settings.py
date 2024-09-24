from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @property
    def DB_URL(self):
        if self.MODE == 'DEV':
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@postgres_warehouse:5432/{self.DB_NAME}"
        return "sqlite+aiosqlite:///:memory:"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
