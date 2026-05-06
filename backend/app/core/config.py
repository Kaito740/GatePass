from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OLLAMA_URL: str = "http://ollama:11434"
    N8N_WEBHOOK_URL: str = "http://n8n:5678/webhook"

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignora variables del .env que no están declaradas aquí


settings = Settings()
