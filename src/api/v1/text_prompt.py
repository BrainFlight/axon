from typing import Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter

from services.text_prompt_service import text_prompt_service


router = APIRouter(prefix="/v1/text_prompt")


class TextPromptV1PostRequest(BaseModel):
    model_name: str
    prompt_format_name: str
    prompt_args: Optional[dict]
    model_args: Optional[Dict[str, Any]] = None


class TextPromptV1PostResponse(BaseModel):
    response: Dict[str, Any]


@router.post("/")
def text_prompt(body: TextPromptV1PostRequest):
    """Text prompt endpoint."""
    response = text_prompt_service(
        body.model_name,
        body.prompt_format_name,
        body.prompt_args,
        body.model_args,
    )

    return TextPromptV1PostResponse(response=response)
