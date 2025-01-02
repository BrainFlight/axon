from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/v1/multimodal_prompt")


class MultimodalPromptV1Request(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    stop: list
    image: str


class MultimodalPromptV1Response(BaseModel):
    response: str


@router.post("/")
async def multimodal_prompt(body: MultimodalPromptV1Request):
    return JSONResponse(content={"response": "Multimodal Prompt Response"})
