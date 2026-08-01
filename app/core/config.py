from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


class Config:
    """Application configuration."""

    APP_NAME = "CyberRAG"
    APP_VERSION = "0.1.0"

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    VECTOR_DB_PATH = "storage/vectorstore"
    DATASET_PATH = "storage/datasets"
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    DEBUG = True


config = Config()
