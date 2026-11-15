"""The application serves exactly the operations its API contract declares."""

import json
from pathlib import Path

from main import app

METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace", "query"}


def operations(document: dict) -> set[tuple[str, str]]:
    return {(path, method) for path, item in document["paths"].items() for method in item if method in METHODS}


def test_the_application_implements_the_contract() -> None:
    contract = json.loads((Path(__file__).parent.parent / "openapi.json").read_text(encoding="utf-8"))
    assert operations(app.openapi()) == operations(contract)
