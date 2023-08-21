from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.routers import links

app = FastAPI()
app.include_router(links.router)

logger.remove()
logger.add(
    "log.log",
    colorize=False,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="DEBUG",
)


@app.get("/")
def root():
    return "Welcome to API for audio to text converting"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
