from pydantic import BaseSettings
from yarl import URL


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"
    SECRET: str = "SECRET"

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "fastapi"

    @property
    def DATABASE_URI(self) -> URL:
        return URL.build(
            scheme="mysql+aiomysql",
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            path=f"/{self.MYSQL_DATABASE}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
