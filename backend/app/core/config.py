# keeps secrets and paths out of code. Consistent with 12-factor app standards.

from pydantic import BaseSettings

class Settings(BaseSettings):
    chroma_dir: str = './chroma_db',
    embedding_model: str = 'all-MiniLM-L6-v2',
    max_upload_mb: int = 100
    api_key: str = 'local-dev-key'

    class Config:
     env_file: '.env'

settings = Settings()

