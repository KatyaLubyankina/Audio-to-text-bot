from fastapi import FastAPI

from src.routers import links

app = FastAPI()
app.include_router(links.router)


@app.get("/")
def root():
    """Endpoint for welcome message."""
    return "Welcome to API for audio to text converting"
