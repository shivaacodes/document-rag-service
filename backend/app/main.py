from fastapi import FastAPI
from .api import routes_upload
from .metrics.prometheus import metrics_app
from .core.logging import setup_logging

logger = setup_logging()

app = FastAPI(title="document-rag-service")

app.include_router(routes_upload.router, prefix="/upload", tags=["upload"])
# app.include_router(routes_query.router, prefix="/query", tags=["query"])
# app.include_router(routes_health.router, tags=["health"])

app.mount("/metrics", metrics_app)

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

