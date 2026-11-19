import path from "node:path"

import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vitest/config"

// The test contract. It is separate from the build configuration so application code cannot narrow what is tested.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(import.meta.dirname, "./src") } },
  test: {
    environment: "jsdom",
    pool: "threads",
    include: ["src/**/__tests__/**/*.test.{ts,tsx}"],
    setupFiles: ["./src/test-setup.ts"],
    allowOnly: false,
    passWithNoTests: false
  }
})
