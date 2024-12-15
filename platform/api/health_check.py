from fastapi import APIRouter, JSONResponse, status

router = APIRouter()

@router.get("/health")
def health_check():
    """Health Check Endpoint."""
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
