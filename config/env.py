import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "url_shortener")
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "")
    MONGODB_MAX_RETRIES: int = int(os.getenv("MONGODB_MAX_RETRIES", "3"))
    MONGODB_RETRY_DELAY: int = int(os.getenv("MONGODB_RETRY_DELAY", "2"))


settings = Settings()
