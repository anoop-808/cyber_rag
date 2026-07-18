from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class Config:
    """Application configuration."""

    APP_NAME = "CyberRAG"

    APP_VERSION = "0.1.0"

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    VECTOR_DB_PATH = "storage/vectorstore"

    DATASET_PATH = "storage/datasets"

    DEBUG = True


config = Config()
