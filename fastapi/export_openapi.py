"""Write the OpenAPI document of the service to openapi.json."""

import json
from pathlib import Path

from main import app

Path("openapi.json").write_text(json.dumps(app.openapi(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
