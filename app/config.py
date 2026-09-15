from pydantic_settings import BaseSettings ,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "RAG-based VCL Intelligence Platform"
    gemini_api_key: str=""
    gemini_chat_model: str="gemini-3.6-flash"
    gemini_embed_model: str="text-embedding-004"
    data_dir: str = "data"
    chunk_size: int = 1000
    chunk_overlap: int = 150
    retrieval_top_k: int = 4
    max_upload_mb: int = 10


settings = Settings()