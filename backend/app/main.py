from fastapi import FastAPI
from .api import routes_upload, routes_query, routes_generate, routes_health
from .metrics.prometheus import metrics_app
from .core.logging import setup_logging
from .tracing import setup_tracing

logger = setup_logging()

tracer = setup_tracing()
app = FastAPI(title="document-rag-service")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_upload.router, prefix="/upload", tags=["upload"])
app.include_router(routes_query.router, prefix="/api/query", tags=["query"])
app.include_router(routes_generate.router, prefix="/api", tags=["generate"])
app.include_router(routes_health.router, tags=["health"])

app.mount("/metrics", metrics_app)

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

