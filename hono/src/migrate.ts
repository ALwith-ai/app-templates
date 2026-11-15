import path from "node:path"

import { runner } from "node-pg-migrate"

import { requiredEnvironment } from "./environment"

const applied = await runner({
  databaseUrl: requiredEnvironment("DATABASE_MIGRATION_URL"),
  dir: path.join(import.meta.dirname, "migrations"),
  migrationsTable: "pgmigrations",
  migrationsSchema: "alwith_migrations",
  createMigrationsSchema: true,
  direction: "up",
  checkOrder: true,
  singleTransaction: true,
  noLock: false
})
console.log(JSON.stringify({ event: "alwith.service.migrated", applied: applied.map((migration) => migration.name) }))
