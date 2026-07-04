# Pitfalls

- **Theme not applied:** a component looks unstyled when the theme provider is
  missing at the app root. Ensure the M3 theme is set up in `app.config.ts`.
- **Hard-coded colors** break dark mode. Always go through M3 tokens.
- **SSR/hydration mismatch:** avoid reading `window`/`document` during component
  construction; guard with `afterNextRender()`.
- **Storybook drift:** a component changed without updating its story will fail
  the visual catalog build.
