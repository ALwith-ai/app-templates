# FastAPI service

Stack: Python 3.15, uv, FastAPI, Pydantic, PostgreSQL (psycopg, Alembic), pytest, Ruff, ty.

```sh
uv sync
DATABASE_MIGRATION_URL=postgresql://... uv run python migrate.py
DATABASE_URL=postgresql://... uv run uvicorn main:app --reload
uv run pytest
uv run python build.py
```

## Layout

| File | What goes there |
| --- | --- |
| `openapi.json` | The API contract. The application serves exactly its operations; `tests/test_contract.py` checks that |
| `main.py` | The application and its routes. Give each area of the API its own module with an `APIRouter` and include it here |
| `models.py` | Pydantic models of the API boundary. Every model extends `Record`, which strips whitespace and rejects unknown fields |
| `config.py` | Settings read from the environment and `.env`. One typed field for each value the service reads |
| `database.py` | The connection pool, `request_identity` for queries on behalf of an authenticated subject, and the runtime role check |
| `migrations/versions/` | Alembic migrations, one per schema change. Applied migrations are never edited |
| `tests/` | pytest tests |
| `server.py` | Serves a build: checks the database role, listens, announces the address, serves `/healthz` |
| `migrate.py` | Applies all pending migrations in one transaction and reports which ran |
| `build.py` | Lints, formats and type checks, then writes what a deployment runs to `dist/` |

## Database

- Two roles. Migrations connect with `DATABASE_MIGRATION_URL`, a role that owns the schema. The service connects with `DATABASE_URL`, a role that does not own tables, is not a superuser and has no BYPASSRLS. `server.py` refuses to start otherwise.
- Every table in `public` the service can use has row-level security. Policies read the subject with `current_setting('app.subject', true)`; a missing subject matches nothing.
- Queries for a subject go through `request_identity(subject)`: one transaction on one connection, with the subject set for that transaction only, so it never reaches the next request on the same pooled connection.
- The subject comes from verified authentication, never from a request field.
- Money is an integer of the smallest currency unit or an exact `numeric`. Idempotency and state rules are database constraints.

## Running a build

```sh
cd dist
DATABASE_MIGRATION_URL=postgresql://... uv run --frozen --no-dev python migrate.py
DATABASE_URL=postgresql://... BUILD_ID=... SERVICE_HOST=127.0.0.1 SERVICE_PORT=0 uv run --frozen --no-dev python server.py
```

Once listening, `server.py` writes one JSON line, `{"event": "service.ready", "url": ..., "buildId": ...}`, and `GET /healthz` returns `{"buildId": ...}` after a database round trip. With `SERVICE_MANAGED=true` the service stops when its standard input closes.

## Rules the template follows

- Pydantic validates at the boundary only: requests, responses, settings and data from outside. Inside the service, pass the validated objects on.
- Settings fail the start. A missing or wrong value stops the service before the first request instead of surfacing later.
- `待填写` marks a slot that is not filled in yet (the title and description in `main.py` and `openapi.json`).
