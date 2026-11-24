// A standard Storybook configuration from the template. The project may change it.
import path from "node:path"

import { defineMain } from "@storybook/react-vite/node"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"

export default defineMain({
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-docs"],
  framework: "@storybook/react-vite",
  // TypeScript 7.0 has no compiler API for the docs engine, so Controls and the Docs args table read TypeScript 6
  typescript: { docgenSpecifier: "@typescript/typescript6" },
  async viteFinal(config) {
    const { mergeConfig } = await import("vite")
    return mergeConfig(config, {
      plugins: [react(), tailwindcss()],
      resolve: { alias: { "@": path.resolve(import.meta.dirname, "../src") } }
    })
  }
})
