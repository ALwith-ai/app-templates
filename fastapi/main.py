"""The service: application, lifespan and routes."""

from contextlib import asynccontextmanager
lazy from collections.abc import AsyncGenerator

from fastapi import FastAPI

from database import open_pool


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    async with open_pool():
        yield


app = FastAPI(lifespan=lifespan, title="待填写", version="0.1.0", description="待填写")
