from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.experiment import router as experiment_router
from api.image_text_prompt import router as image_text_prompt_router
from api.text_prompt import router as text_prompt_router


app = FastAPI()

app.include_router(experiment_router)
app.include_router(image_text_prompt_router)
app.include_router(text_prompt_router)

