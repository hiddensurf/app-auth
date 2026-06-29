from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    database_user:str
    database_password:str
    database_port:int
    database_db:str
    database_host:str
    secret_key:str  
    algorithm:str="HS256"
    time_to_expire:int=30
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
settings=Settings() 