# FastAPI service

Stack: Python 3.15, uv, FastAPI, Pydantic, pydantic-settings, pytest, Ruff, ty.

```sh
uv sync
uv run uvicorn main:app --reload
uv run pytest
ruff check && ruff format --check && ty check
```

## Layout

| File | What goes there |
| --- | --- |
| `main.py` | The application, its lifespan and routes. Give each area of the API its own module with an `APIRouter` and include it here |
| `models.py` | Pydantic models of the API boundary. Every model extends `Record`, which strips whitespace and rejects unknown fields |
| `config.py` | Settings read from the environment and `.env`. One typed field for each value the service reads |
| `export_openapi.py` | Writes `openapi.json` from the application |
| `tests/` | pytest tests against the real application through `TestClient` |

## Rules the template follows

- Pydantic validates at the boundary only: requests, responses, settings and data from outside. Inside the service, pass the validated objects on.
- Settings fail the start. A missing or wrong value stops the service before the first request instead of surfacing later.
- No database is included. Add one when plain files cannot meet a stated need.
- `待填写` marks a slot that is not filled in yet (the title and description in `main.py`).
