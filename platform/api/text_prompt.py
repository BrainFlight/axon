import json
from typing import List, Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter

from services.text_prompt_service import text_prompt_service


class TextPromptInput(BaseModel):
    model_name: str
    prompt_format_name: str
    prompt_args: Optional[dict]
    # max_tokens: Optional[int]
    # temperature: Optional[float]
    # top_p: Optional[float]
    # frequency_penalty: Optional[float]
    # presence_penalty: Optional[float]
    # stop: Optional[List[str]]
    # load_to_cache: Optional[bool] = False

class TextPromptV1PostResponse(BaseModel):
    response : Dict[str, Any]

router = APIRouter()

@router.post("/v1/text_prompt")
def text_prompt(body: TextPromptInput):
    """Text Prompt Endpoint."""
    # TODO: Validate input

    response = text_prompt_service(
        body.model_name, 
        body.prompt_format_name, 
        body.prompt_args
    )

    return TextPromptV1PostResponse(response={"Response": response})
