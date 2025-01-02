from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter(prefix="/v1/training_job")


class TrainingJobV1GetResponse(BaseModel):
    job_status: str


@router.get("/{job_id}")
def get_training_job_status(job_id: int):
    """Get training job status endpoint."""
    return TrainingJobV1GetResponse(job_id=job_id)


class TrainingJobV1PostRequest(BaseModel):
    job_name: str


class TrainingJobV1PostResponse(BaseModel):
    job_id: int


@router.post("/")
def start_training_job(body: TrainingJobV1PostRequest):
    """Start new training job endpoint."""
    return TrainingJobV1PostResponse(job_id=-1)
