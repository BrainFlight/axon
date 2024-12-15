from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
def health_check():
    """Health Check Endpoint."""
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
