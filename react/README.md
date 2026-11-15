# React + TypeScript + Vite

## Storybook

`bun run storybook` shows every page together with its product definition.

This template provides a minimal setup to get React working in Vite with HMR and Bun lint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Code checks

Use Bun Canary for `bun lint` and `bun lint --fix`. Formatting uses `bun fmt`.
Lint rules live in `bunfig.toml`; no separate linter package is required.
