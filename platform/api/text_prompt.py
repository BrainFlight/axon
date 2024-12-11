import json
from typing import List, Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter

from services.text_prompt_service import text_prompt_service


class prompt_body(BaseModel):
    model_name: str
    prompt: str
    prompt_args: Optional[dict]
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]
    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]
    stop: Optional[List[str]]
    # load_to_cache: Optional[bool] = False

class api_response(BaseModel):
    response : Dict[str, Any]

router = APIRouter()

@router.post("/v1/text_prompt")
def text_prompt(body: prompt_body):
    """Text Prompt Endpoint."""
    # TODO: Validate input
    response = text_prompt_service(body.prompt)

    return api_response(response=response)
