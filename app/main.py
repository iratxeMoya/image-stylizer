from fastapi import FastAPI
from .api import router

app = FastAPI(
    title="AI Image Style Transfer",
    description="A simple API for applying styles to images using pre-trained models",
    version="1.0.0",
)

app.include_router(router)