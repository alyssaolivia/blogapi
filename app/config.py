from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    jwt_key: str
    jwt_alg: str
    jwt_interval: int

    class Config:
        env_file = ".env"

settings = Settings()
