"""Serve a build: check the database role, listen, and announce the address on stdout.

Configuration comes from the environment only:

- `BUILD_ID`: the build being served, returned by the health check.
- `SERVICE_HOST`, `SERVICE_PORT`: where to listen. Port 0 picks a free port; the announcement carries it.
- `SERVICE_MANAGED`: when true, the service stops once its standard input closes, so it cannot outlive
  the process that started it.

Once listening, the service writes one JSON line `{"event": "service.ready", "url": ..., "buildId": ...}`.
"""

import asyncio
import json
import sys
import threading
lazy from socket import socket

import uvicorn
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from database import get_pool, verify_runtime_role
from main import app

HEALTH_PATH = "/healthz"


class ServerSettings(BaseSettings):
    """What to serve and where."""

    model_config = SettingsConfigDict(extra="ignore", hide_input_in_errors=True)

    build_id: str = Field(min_length=1)
    service_host: str = Field(min_length=1)
    service_port: int = Field(ge=0, le=65535)
    service_managed: bool = False


def announce(event: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(event) + "\n")
    sys.stdout.flush()


class Server(uvicorn.Server):
    """Uvicorn server that announces its address once it listens."""

    def __init__(self, config: uvicorn.Config, build_id: str) -> None:
        """Serve `config` and announce `build_id` with the address."""
        super().__init__(config)
        self.build_id = build_id

    async def startup(self, sockets: list[socket] | None = None) -> None:
        await super().startup(sockets)
        if self.should_exit:
            return
        host, port = self.servers[0].sockets[0].getsockname()[:2]
        announce({"event": "service.ready", "url": f"http://{host}:{port}/", "buildId": self.build_id})


async def serve(settings: ServerSettings) -> None:
    await verify_runtime_role()

    async def health() -> dict[str, str]:
        async with get_pool().connection() as connection:
            await connection.execute("SELECT 1")
        return {"buildId": settings.build_id}

    app.add_api_route(HEALTH_PATH, health, include_in_schema=False)
    server = Server(uvicorn.Config(app, host=settings.service_host, port=settings.service_port), settings.build_id)
    if settings.service_managed:
        loop = asyncio.get_running_loop()

        def stop() -> None:
            server.should_exit = True

        def stop_at_end_of_input() -> None:
            sys.stdin.buffer.read()
            loop.call_soon_threadsafe(stop)

        threading.Thread(target=stop_at_end_of_input, daemon=True).start()
    await server.serve()


if __name__ == "__main__":
    asyncio.run(serve(ServerSettings()))
