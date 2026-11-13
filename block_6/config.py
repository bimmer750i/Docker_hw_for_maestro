from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_DB : str
    DB_HOST : str
    model_config = SettingsConfigDict(env_file=".env")

# Импортируем эту штуку в других файлах, чтобы не делать кучу os.environ
settings = Settings()
