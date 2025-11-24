# It uses API-key auth, covers request size limits, and gives a single place to extend later 
# (JWT/JWKS, rate-limits, IP allowlists, etc).

from fastapi import HTTPException, Header, status
from .config import settings

# API key validation

async def verify_api_key(x_api_key: str = Header(None)):
    """Simple API Key Protection.
    Production: Rotate keys, store in env, use JWKS if scaling externally.
    """
    if settings.api_key is None:
        return # auth disabled for local dev

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing api key",
        )
    
# Request Size limits

MAX_UPLOAD_SIZE_MB = 20

def enforce_request_size(content_length: int | None):
    """ Reject very large file uploads before hitting injestion logic.
    Production: Prevents abuse and accidental uploads.
    """
    if content_length is None:
        return 

    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if content_length > max_bytes:
        raise HTTPException(
            status_code= status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max allowed is {MAX_UPLOAD_SIZE_MB} MB.",
        )
