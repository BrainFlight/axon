from fastapi import APIRouter
from pydantic import BaseModel

class image_text_prompt_body(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    stop: list
    image: str

router = APIRouter()

@router.post("/v1/image_text_prompt")
async def image_text_prompt(body: image_text_prompt_body):
    return body