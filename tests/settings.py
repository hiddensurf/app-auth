from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_PATH=Path(__file__).resolve().parent
class TestSettings(BaseSettings):
    database_user:str
    database_password:str
    database_db:str
    database_port:int
    database_host:str
    model_config=SettingsConfigDict(
        env_file=BASE_PATH/".env.test",
        extra="ignore"
    )
settings=TestSettings()