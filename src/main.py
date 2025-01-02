import logging

import ray
from ray import serve
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import GlobalConfig
from constants import WELCOME_ASCII
from ray_utils.sessionManager import SessionStateManager
from api.v1.experiment import router as experiment_router
from api.v1.multimodal_prompt import router as multimodal_prompt_router
from api.v1.text_prompt import router as text_prompt_router
from api.v1.training_job import router as training_job_router


config = GlobalConfig()

app = FastAPI(
    title="BrainFlight Axon",
    description="Enabling accessible and explainable human-robot \
        interaction through your favourite large language models",
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


@serve.deployment()
@serve.ingress(app)
class APIDeployment:
    def __init__(self, model_directory: str):
        self.model_directory = model_directory
        self.model_manager = SessionStateManager.remote()
        self.logger = logging.getLogger(__name__)

        app.include_router(experiment_router)
        app.include_router(multimodal_prompt_router)
        app.include_router(text_prompt_router)
        app.include_router(training_job_router)

    @app.get("/health")
    def health_check(self):
        """Health Check Endpoint."""
        return JSONResponse(status_code=status.HTTP_200_OK, content={})


if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)
    serve.start()

    model_directory = "/path/to/model/directory"

    deployment = APIDeployment.bind(model_directory)
    serve.run(deployment)

    print(WELCOME_ASCII)
    print(
        f"DOCS:     Swagger docs available at: http://{config.api_host}:{config.api_port}/docs"
    )
    print(f"DOCS:     Ray dashboard available at: http://{config.api_host}:8265")
    if ray.is_initialized():
        uvicorn.run(app, host=config.api_host, port=config.api_port, log_level="info")
