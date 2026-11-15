// A standard Storybook configuration from the template. The project may change it.
import path from "node:path"

import type { StorybookConfig } from "@storybook/react-vite"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"

const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-docs"],
  framework: "@storybook/react-vite",
  async viteFinal(config) {
    const { mergeConfig } = await import("vite")
    return mergeConfig(config, {
      plugins: [react(), tailwindcss()],
      resolve: { alias: { "@": path.resolve(import.meta.dirname, "../src") } }
    })
  }
}

export default config
