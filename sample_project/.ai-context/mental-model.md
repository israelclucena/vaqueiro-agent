# Mental model

NG-M3 is an Angular component library and demo app implementing a **Material
Design 3** design system. It ships reusable UI components, a theming layer built
on M3 design tokens, and a Storybook catalog.

- `src/lib/` - the reusable components (one folder per component).
- `src/theme/` - M3 tokens, palettes and the theme setup.
- `src/app/` - a demo application that consumes the library.
- Components are **standalone** (no NgModules) and composed via `imports`.

Rendering flow: the theme layer generates CSS custom properties from M3 tokens;
components consume those properties, so restyling means changing tokens, not
component code.
