import { globSync } from "node:fs"
import path from "node:path"

import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vitest/config"

/** Every page is its own HTML file, nested directories included; dependencies and build output are left out. */
function htmlEntries(): Record<string, string> {
  return Object.fromEntries(
    globSync("**/*.html", {
      cwd: __dirname,
      exclude: ["node_modules/**", "dist/**", ".git/**", ".alwith/**"]
    })
      .sort()
      .map((name) => [name.slice(0, -".html".length), path.resolve(__dirname, name)])
  )
}

export default defineConfig({
  // A preview host may serve the project under a sub-path, so assets use a relative base
  base: "./",
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
  build: { outDir: "dist", rolldownOptions: { input: htmlEntries() } },
  /**
   * Unit tests. Each page has one test file, `src/__tests__/<page>.test.tsx`.
   * End-to-end acceptance tests do not live here: they belong in a separate test repository.
   */
  test: { environment: "jsdom", include: ["src/**/__tests__/**/*.test.{ts,tsx}"] }
})
