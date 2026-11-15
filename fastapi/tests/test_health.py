import pytest
from pydantic import ValidationError
lazy from fastapi.testclient import TestClient

from models import Health


def test_health_reports_the_running_build(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok", "build_id": "development"}


def test_unknown_fields_are_rejected_at_the_boundary() -> None:
    with pytest.raises(ValidationError):
        Health.model_validate({"status": "ok", "build_id": "development", "unexpected": True})
