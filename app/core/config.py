from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"
    SECRET: str = "SECRET"

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DATABASE: str = "fastapi"
    DATABASE_URI: str = None  # type: ignore

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return (
            f"mysql+aiomysql://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}@{values.get('MYSQL_HOST')}:"
            f"{values.get('MYSQL_PORT')}/{values.get('MYSQL_DATABASE')}"
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
