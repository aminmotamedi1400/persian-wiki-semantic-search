from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "wiki_titles_fa"
    model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
    batch_size: int = 128
    max_rows: int = 5000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")