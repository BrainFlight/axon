from fastapi import APIRouter
from pydantic import BaseModel


class multimodal_prompt_body(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    stop: list
    image: str


router = APIRouter()


@router.post("/v1/multimodal_prompt")
async def multimodal_prompt(body: multimodal_prompt_body):
    return body
