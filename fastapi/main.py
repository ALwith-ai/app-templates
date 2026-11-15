"""The service: application, lifespan and routes."""

from contextlib import asynccontextmanager
lazy from collections.abc import AsyncGenerator

from fastapi import FastAPI

from config import get_settings
from models import Health


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    # Read the settings before the first request, so that a wrong configuration stops the start.
    get_settings()
    yield


app = FastAPI(lifespan=lifespan, title="待填写", version="0.1.0", description="待填写")


@app.get("/api/health", response_model=Health)
def health() -> Health:
    return Health(status="ok", build_id=get_settings().build_id)
