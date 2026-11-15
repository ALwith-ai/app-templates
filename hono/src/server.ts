import { app } from "./app"
import { database, verifyRuntimeDatabaseRole } from "./database"
import { requiredEnvironment } from "./environment"

const buildId = requiredEnvironment("ALWITH_BUILD_ID")
const hostname = requiredEnvironment("ALWITH_SERVICE_HOST")
const port = Number(requiredEnvironment("ALWITH_SERVICE_PORT"))
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error("The service port is not valid")
await verifyRuntimeDatabaseRole()

const server = Bun.serve({
  hostname,
  port,
  async fetch(request) {
    if (new URL(request.url).pathname === "/.well-known/alwith/health") {
      await database.query("SELECT 1")
      return Response.json({ buildId })
    }
    return app.fetch(request)
  }
})
console.log(JSON.stringify({ event: "alwith.service.ready", url: server.url.href, buildId }))

async function stop() {
  await server.stop()
  await database.end()
}
process.once("SIGTERM", stop)
process.once("SIGINT", stop)

// A managing process holds the write end of stdin. When it exits, EOF stops the service, so no orphan is left behind.
if (process.env.ALWITH_SERVICE_MANAGED === "1") {
  void Bun.stdin.stream().pipeTo(new WritableStream()).then(stop)
}
