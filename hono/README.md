# Hono service

Stack: Bun, TypeScript, Hono, PostgreSQL, node-pg-migrate, Vitest. Dependencies and scripts always run through Bun.

## What you write and what the template owns

The template owns `build.ts`, `vitest.config.ts`, `src/server.ts`, `src/migrate.ts`, `src/database.ts` and `src/environment.ts`. You implement the product's OpenAPI in `src/app.ts` and your own modules, write the SQL migrations in `migrations/`, and write unit tests in `src/__tests__/`. `openapi.json` is the API contract of the product; do not define a second one.

## Database

The service uses `DATABASE_URL` and migrations use `DATABASE_MIGRATION_URL`. Business tables live in the `public` schema. The request identity comes from verified authentication, never from a user or tenant the request passes in directly. The service must not connect as the database owner, a superuser or a `BYPASSRLS` role. SQL that depends on the identity goes through `withRequestIdentity` in `src/database.ts`, which runs it on one transaction connection. Row-level security reads the identity from `current_setting('alwith.subject', true)` and must refuse when it is missing. The local identity is not kept across pooled requests. Store money as integers of the smallest currency unit or as exact decimals, and enforce idempotency and state rules in the database itself.

## Build and run

`build` produces `dist/server.mjs`, `dist/migrate.mjs`, `dist/openapi.json` and `migrations/`. The host injects `ALWITH_BUILD_ID`, `ALWITH_SERVICE_HOST` and `ALWITH_SERVICE_PORT` at deployment. The health endpoint returns the running version and checks the database connection. Logs must not contain database passwords, access tokens or vendor keys.

## Tests

Unit tests are yours and are run for real. Independent HTTP acceptance tests belong in a separate test repository. When real configuration or a vendor capability is missing, report it; do not let a test double stand in for a successful payment, settlement or production deployment.
