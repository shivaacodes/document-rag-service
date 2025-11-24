from fastapi import FastAPI
from .api import routes_upload, routes_query, routes_generate
from .metrics.prometheus import metrics_app
from .core.logging import setup_logging

logger = setup_logging()

app = FastAPI(title="document-rag-service")

app.include_router(routes_upload.router, prefix="/upload", tags=["upload"])
app.include_router(routes_query.router, prefix="/api/query", tags=["query"])
app.include_router(routes_generate.router, prefix="/api", tags=["generate"])

app.mount("/metrics", metrics_app)

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

