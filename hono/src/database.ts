import { Pool, type PoolClient } from "pg"

import { requiredEnvironment } from "./environment"

export const database = new Pool({ connectionString: requiredEnvironment("DATABASE_URL") })

// The identity comes from the authenticated boundary. Every query reuses one transaction connection, so the local setting cannot leak into the next request.
export async function withRequestIdentity<Result>(
  subject: string,
  operation: (transaction: PoolClient) => Promise<Result>
): Promise<Result> {
  if (subject.trim() === "") throw new Error("A database transaction needs the authenticated request identity")
  const transaction = await database.connect()
  try {
    await transaction.query("BEGIN")
    await transaction.query("SELECT set_config('alwith.subject', $1, true)", [subject])
    const result = await operation(transaction)
    await transaction.query("COMMIT")
    return result
  } catch (error) {
    await transaction.query("ROLLBACK")
    throw error
  } finally {
    transaction.release()
  }
}

export async function verifyRuntimeDatabaseRole(): Promise<void> {
  const role = await database.query<{ rolsuper: boolean; rolbypassrls: boolean }>(
    "SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user"
  )
  const [runtimeRole] = role.rows
  if (runtimeRole === undefined || runtimeRole.rolsuper || runtimeRole.rolbypassrls) {
    throw new Error("The service must not connect as a superuser or a BYPASSRLS role")
  }
  const unsafeTables = await database.query<{ table_name: string }>(`
    SELECT quote_ident(namespace.nspname) || '.' || quote_ident(relation.relname) AS table_name
    FROM pg_class relation JOIN pg_namespace namespace ON namespace.oid = relation.relnamespace
    WHERE relation.relkind IN ('r', 'p')
      AND namespace.nspname = 'public'
      AND has_table_privilege(relation.oid, 'SELECT,INSERT,UPDATE,DELETE')
      AND (NOT relation.relrowsecurity OR pg_has_role(relation.relowner, 'USAGE'))
  `)
  if (unsafeTables.rows.length > 0) {
    throw new Error(`The service connection can bypass row isolation on: ${unsafeTables.rows.map((row) => row.table_name).join(", ")}`)
  }
}
