import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.experiment import router as experiment_router
from api.image_text_prompt import router as image_text_prompt_router
from api.text_prompt import router as text_prompt_router
from config import GlobalConfig


config = GlobalConfig()

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(experiment_router)
app.include_router(image_text_prompt_router)
app.include_router(text_prompt_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
