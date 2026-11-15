"""Alembic environment: migrations run on the connection `migrate.py` opened, inside its transaction."""

from alembic import context
from sqlalchemy import text

from migrate import VERSION_SCHEMA

if context.is_offline_mode():
    msg = "Migrations run against the database; offline SQL generation is not supported"
    raise RuntimeError(msg)

connection = context.config.attributes["connection"]
# Concurrent deployments wait for each other instead of applying the same migration twice.
connection.execute(text("SELECT pg_advisory_xact_lock(hashtext('alembic'))"))
connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {VERSION_SCHEMA}"))
context.configure(connection=connection, version_table_schema=VERSION_SCHEMA, transactional_ddl=True)
with context.begin_transaction():
    context.run_migrations()
