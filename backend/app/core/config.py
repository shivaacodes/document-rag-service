# keeps secrets and paths out of code. Consistent with 12-factor app standards.

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    chroma_dir: str = './chroma_db'
    chroma_server_host: str = 'chroma'
    chroma_server_http_port: int = 8000
    embedding_model: str = 'all-MiniLM-L6-v2'
    max_upload_mb: int = 100
    api_key: str = 'local-dev-key'
    otel_exporter_otlp_traces_endpoint: str = 'http://localhost:4318/v1/traces'

settings = Settings()

