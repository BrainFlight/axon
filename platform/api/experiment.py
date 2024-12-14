import json
from typing import List, Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter()


class NewExperimentInput(BaseModel):
    name: str
    # TODO: Modify these as needed
    # prompt: str
    # max_tokens: int
    # temperature: float
    # top_p: float
    # frequency_penalty: float
    # presence_penalty: float
    # stop: list
    # model: str
    # output_format: str
    # pipeline: str

class ExperimentV1PostResponse(BaseModel):
    response : Dict[str, Any]

@router.post("/v1/experiment")
def new_experiment(body: NewExperimentInput):
    """Endpoint for creating a new experiment."""
    return ExperimentV1PostResponse(response={"Response": "Success"})
