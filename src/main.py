from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import GlobalConfig
from constants import WELCOME_ASCII
from api.health_check import router as health_check_router
from api.experiment import router as experiment_router
from api.multimodal_prompt import router as multimodal_prompt_router
from api.text_prompt import router as text_prompt_router


config = GlobalConfig()

app = FastAPI(
    title="BrainFlight Axon",
    description="Enabling accessible and explainable human-robot interaction through your favourite large language models",
    summary="",
    version="0.1.0",
)

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
app.include_router(multimodal_prompt_router)
app.include_router(text_prompt_router)
app.include_router(health_check_router)

if __name__ == "__main__":
    import uvicorn

    print(WELCOME_ASCII)
    print(f"docs available at: http://{config.api_host}:{config.api_port}/docs")
    uvicorn.run(app, host=config.api_host, port=config.api_port)
