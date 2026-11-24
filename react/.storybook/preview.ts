// A standard Storybook configuration from the template. The project may change it.
import "../src/index.css"

import addonDocs from "@storybook/addon-docs"
import { definePreview } from "@storybook/react-vite"

export default definePreview({ addons: [addonDocs()] })
