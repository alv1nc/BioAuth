import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_NAME: str = "Bio-Auth API"
    DEBUG_MODE: bool = True

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SPEECHBRAIN_DIR: str = os.path.join(os.getcwd(),"pretrained_model")

    class Config:
        env_file = ".env"
settings = Settings()
