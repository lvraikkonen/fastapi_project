from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    # Load .env file
    load_dotenv()

    # Development Database URL
    DEVELOPMENT_DATABASE_URL: str = os.getenv("DEV_DATABASE_URL", "sqlite:///./development.db")

    # Test Database URL
    TESTING_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "sqlite:///./testing.db")

    # Production Database URL
    PRODUCTION_DATABASE_URL: str = os.getenv("PROD_DATABASE_URL", "sqlite:///./prod.db")

    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # model_config = ConfigDict(env_file=".env")


settings = Settings()
