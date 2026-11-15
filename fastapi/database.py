"""PostgreSQL access: one connection pool, and transactions that carry the authenticated subject.

Row-level security policies read the subject with `current_setting('app.subject', true)`. The subject
is set inside the transaction (`set_config(..., true)`), so it ends with the transaction and never
reaches the next request that borrows the same pooled connection.
"""

from contextlib import asynccontextmanager
from functools import cache
lazy from collections.abc import AsyncGenerator

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

from config import get_settings


@cache
def get_pool() -> AsyncConnectionPool:
    return AsyncConnectionPool(str(get_settings().database_url), open=False)


@asynccontextmanager
async def open_pool() -> AsyncGenerator[AsyncConnectionPool]:
    """Open the pool for the lifetime of the application and close it on shutdown.

    Yields:
        The open pool.

    """
    async with get_pool() as pool:
        yield pool


@asynccontextmanager
async def request_identity(subject: str) -> AsyncGenerator[AsyncConnection]:
    """Run queries for an authenticated subject in one transaction on one connection.

    Yields:
        The connection, inside the transaction.

    Raises:
        ValueError: The subject is empty. Identity comes from verified authentication, never from request data.

    """
    if not subject.strip():
        msg = "The transaction has no authenticated subject"
        raise ValueError(msg)
    async with get_pool().connection() as connection, connection.transaction():
        await connection.execute("SELECT set_config('app.subject', %s, true)", (subject,))
        yield connection


async def verify_runtime_role() -> None:
    """Refuse to serve through a connection that could bypass row-level security.

    Raises:
        RuntimeError: The role is a superuser or has BYPASSRLS, or a public table it can use is not isolated.

    """
    async with await AsyncConnection.connect(str(get_settings().database_url)) as connection:
        role = await (
            await connection.execute("SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user")
        ).fetchone()
        if role is None or role[0] or role[1]:
            msg = "The service must not connect as a superuser or a BYPASSRLS role"
            raise RuntimeError(msg)
        unsafe = await (
            await connection.execute("""
                SELECT quote_ident(namespace.nspname) || '.' || quote_ident(relation.relname)
                FROM pg_class relation JOIN pg_namespace namespace ON namespace.oid = relation.relnamespace
                WHERE relation.relkind IN ('r', 'p')
                  AND namespace.nspname = 'public'
                  AND has_table_privilege(relation.oid, 'SELECT,INSERT,UPDATE,DELETE')
                  AND (NOT relation.relrowsecurity OR pg_has_role(relation.relowner, 'USAGE'))
            """)
        ).fetchall()
        if unsafe:
            msg = f"The service connection can bypass row-level security on: {', '.join(row[0] for row in unsafe)}"
            raise RuntimeError(msg)
