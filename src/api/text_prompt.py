from typing import Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter

from services.text_prompt_service import text_prompt_service


class TextPromptInput(BaseModel):
    model_name: str
    prompt_format_name: str
    prompt_args: Optional[dict]
    model_args: Optional[Dict[str, Any]] = None


class TextPromptV1PostResponse(BaseModel):
    response: Dict[str, Any]


router = APIRouter()


@router.post("/v1/text_prompt")
def text_prompt(body: TextPromptInput):
    """Text Prompt Endpoint."""
    # TODO: Validate input

    response = text_prompt_service(
        body.model_name,
        body.prompt_format_name,
        body.prompt_args,
        body.model_args,
    )

    return TextPromptV1PostResponse(response={"Response": response})
