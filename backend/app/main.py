from fastapi import FastAPI
from app.api import routes_upload, routes_query, routes_health

app = FastAPI(title="document-rag-service")
# app.include_router(routes_upload.router, prefix="/upload", tags=["upload"])
# app.include_router(routes_query.router, prefix="/query", tags=["query"])
# app.include_router(routes_health.router, tags=["health"])

