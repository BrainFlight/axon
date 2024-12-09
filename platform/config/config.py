import os

import dotenv
from pydantic import ConfigDict

dotenv.load_dotenv()

class GlobalConfig:
    def __init__(self):
        # API
        self.api_port: int = os.getenv("API_PORT", 8000)
        self.api_host: str = os.getenv("API_HOST", "http://localhost")

        # Model Interface API Keys
        self.openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
        self.cohere_api_key: str | None = os.getenv("COHERE_API_KEY")

