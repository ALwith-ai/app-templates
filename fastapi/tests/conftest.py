lazy from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

import config
from main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    # Tests read the environment they set, never a developer's .env file.
    config.get_settings.cache_clear()
    monkeypatch.setattr(config.Settings, "model_config", {**config.Settings.model_config, "env_file": None})
    try:
        with TestClient(app) as client:
            yield client
    finally:
        config.get_settings.cache_clear()
