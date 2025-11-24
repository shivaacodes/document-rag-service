# Accept file upload, Validate API key, Validate file size / type, Call ingestion_service.ingest(...), 
#.., Update Prometheus counters, Return JSON respons

# thin api wrapper

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from ..services.ingestion import ingestion_service
from ..core.config import settings
from ..core.security import verify_api_key
from ..metrics.prometheus import INGEST_COUNTER,REQUEST_LATENCY

router = APIRouter()

@router.post("")
async def upload_document(
    file: UploadFile = File(...),
    _: None = Depends(verify_api_key)):
    # endpoint-level latency timer
    with REQUEST_LATENCY.labels(endpoint="/upload").time():
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        filename = file.filename.lower()

        if not filename.endswith((".pdf",".txt")):
            raise HTTPException(status_code=400, detail="Only pdf/txt allowed")

        file_bytes = await file.read()

        if len(file_bytes) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(status_code=412, detail="File too large")

        try:
            result = await ingestion_service.ingest(file_bytes,filename)
            INGEST_COUNTER.inc()
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


