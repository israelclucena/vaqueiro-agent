# Conventions

- **Standalone components only.** No NgModules. Declare dependencies in the
  component `imports` array.
- **Signals for state**, `computed()` for derived state; use RxJS only at async
  boundaries (HTTP, streams).
- **New control flow** (`@if`, `@for`, `@switch`) instead of `*ngIf` / `*ngFor`.
- **Styling via M3 tokens.** Never hard-code colors; reference the CSS custom
  properties emitted by `src/theme/`.
- **Naming:** components `ng-m3-<name>`, files `kebab-case`, inputs/outputs
  `camelCase`. One component per folder with its `.ts`, `.html`, `.scss`, `.stories.ts`.
- Every public component has a Storybook story.
