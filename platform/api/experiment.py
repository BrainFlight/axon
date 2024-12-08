from pydantic import BaseModel
from fastapi import APIRouter
from typing import List

class experiment_body(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    stop: list
    model: str
    output_format: str
    pipeline: str

class experiments(BaseModel):
    experiments: List[experiment_body]


router = APIRouter()

@router.post("/v1/experiment")
async def experiment(body: experiments):
    return body