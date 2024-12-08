from pydantic import BaseModel
from fastapi import APIRouter
from typing import List

class prompt_body(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    stop: List[str]

router = APIRouter()

@router.post("/v1/text_prompt")
async def text_prompt(body: prompt_body):
    return body