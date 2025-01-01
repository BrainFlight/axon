from typing import Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter()


class NewPromptFormatInput(BaseModel):
    prompt_format_name: str
    prompt: str
    prompt_args: Optional[Dict[str, Any]]
    rag_args: Optional[Dict[str, str]]
    metadata: Optional[Dict[str, Any]]
    load_to_cache: bool = False


class NewPromptFormatV1PostResponse(BaseModel):
    response: Dict[str, Any]


@router.post("/v1/prompt_format")
def register_prompt_format(body: NewPromptFormatInput):
    """Text Prompt Endpoint."""
    # TODO: Validate input

    # TODO: Create a new prompt format and load to cache if needed

    return NewPromptFormatV1PostResponse(response={})
