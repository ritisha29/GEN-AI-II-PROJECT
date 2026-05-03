from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "ReviewRadar AI"
    # The directory to store the ChromaDB database
    CHROMA_DB_DIR: str = "./data/chroma_db"
    # The name of the collection in ChromaDB
    COLLECTION_NAME: str = "product_reviews"
    # The model used for generating embeddings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
