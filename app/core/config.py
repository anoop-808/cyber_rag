from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


class Config:
    """Application configuration."""

    APP_NAME = "CyberRAG"
    APP_VERSION = "0.1.0"

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # LLM Interface Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct:free")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "30.0"))
    LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "3"))

    VECTOR_DB_PATH = "storage/vectorstore"
    DATASET_PATH = "storage/datasets"

    DEBUG = True


config = Config()
