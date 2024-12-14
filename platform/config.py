import os

import dotenv
from pydantic import ConfigDict

dotenv.load_dotenv()

class GlobalConfig:
    def __init__(self):
        # API
        self.api_port: int = os.getenv("API_PORT", 8000)
        self.api_host: str = os.getenv("API_HOST", "localhost")

        # Model Interface API Keys
        self.openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
        self.cohere_api_key: str | None = os.getenv("COHERE_API_KEY")

        # AWS and MinIO
        self.aws_access_key_id: str | None = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region_name: str = os.getenv("AWS_REGION_NAME", "us-east-1")
        self.minio_endpoint_url: str | None = os.getenv("MINIO_ENDPOINT_URL")

        # Qdrant Vector DB
        self.qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
