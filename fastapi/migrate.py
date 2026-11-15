"""Apply the database migrations in one transaction and report which ones ran.

Reads `DATABASE_MIGRATION_URL`, a role allowed to change the schema. The service itself connects with
`DATABASE_URL`, a role that is not. On success the script writes one JSON line
`{"event": "service.migrated", "applied": [<revision>, ...]}`.
"""

import json
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, make_url
from sqlalchemy.pool import NullPool

VERSION_SCHEMA = "alembic"


class MigrationSettings(BaseSettings):
    """Where to apply the migrations."""

    model_config = SettingsConfigDict(extra="ignore", hide_input_in_errors=True)

    database_migration_url: PostgresDsn


def migrate(settings: MigrationSettings) -> list[str]:
    config = Config(Path(__file__).parent / "alembic.ini")
    script = ScriptDirectory.from_config(config)
    url = make_url(str(settings.database_migration_url)).set(drivername="postgresql+psycopg")
    with create_engine(url, poolclass=NullPool).begin() as connection:
        context = MigrationContext.configure(connection, opts={"version_table_schema": VERSION_SCHEMA})
        before = context.get_current_heads()
        config.attributes["connection"] = connection
        command.upgrade(config, "heads")
        after = context.get_current_heads()
    return [revision.revision for revision in reversed(list(script.iterate_revisions(after, before)))]


if __name__ == "__main__":
    applied = migrate(MigrationSettings())
    sys.stdout.write(json.dumps({"event": "service.migrated", "applied": applied}) + "\n")
