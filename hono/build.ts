import { cp, mkdir, readdir, rm } from "node:fs/promises"
import path from "node:path"

// Build staging area inside the project. The output is handed over only once it is complete.
const root = import.meta.dirname
const migrations = (await readdir(path.join(root, "migrations"), { withFileTypes: true }))
  .filter((entry) => entry.isFile() && entry.name.endsWith(".sql"))
  .map((entry) => entry.name)
if (migrations.length === 0) throw new Error("No database migration found in migrations/")
for (const name of migrations) {
  if (!/^\d+[\w-]*\.sql$/.test(name)) throw new Error(`A migration file name needs a numeric prefix and a plain identifier: ${name}`)
}
const contract = Bun.file(path.join(root, "openapi.json"))
if (!(await contract.exists())) throw new Error("openapi.json, the API contract of the product, is missing")
await rm(path.join(root, "dist"), { recursive: true, force: true })
await mkdir(path.join(root, "dist"))
await Bun.build({
  entrypoints: [path.join(root, "src/server.ts"), path.join(root, "src/migrate.ts")],
  outdir: path.join(root, "dist"),
  target: "bun",
  naming: "[name].mjs",
  sourcemap: "external"
})
await mkdir(path.join(root, "dist/migrations"))
for (const name of migrations) {
  await cp(path.join(root, "migrations", name), path.join(root, "dist/migrations", name))
}
await Bun.write(path.join(root, "dist/openapi.json"), contract)
