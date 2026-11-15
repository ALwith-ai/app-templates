# App templates

Starting points for the parts of an application. Each directory is a complete project: copy it, install, and build.

| Template | What it is | Stack |
| --- | --- | --- |
| [`react`](react) | Web front end | React, TypeScript, Vite, Tailwind, shadcn, Vitest, Storybook |
| [`genos`](genos) | iOS and Android app | Genos (SwiftUI, Jetpack Compose) |

Templates are named after their framework.

## Use

```sh
cp -R react my-app && cd my-app
bun install
bun run build
```

## Conventions a generator can rely on

A tool that lays out a project from these templates, such as ALwith, can depend on two markers. They are part of the templates' contract, not incidental comments.

- `alwith-skeleton-placeholder` marks a placeholder file (`react/index.html`, `react/src/main.tsx`, `react/src/App.tsx`). A generator replaces or removes these files when it writes the first real page.
- `待填写` is the text of a slot that has not been filled in.

Nothing else in a template refers to the tool that copied it. A template builds and runs on its own.

## Versions

The repository is versioned as a whole. A project should record the version of the template it was created from.
