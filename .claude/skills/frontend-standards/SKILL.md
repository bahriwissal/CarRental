---
name: frontend-standards
description: Coding standards for the React/Vite frontend. Use before writing or reviewing anything in frontend/src.
---

# Frontend standards (React 18 + Vite 4, plain JSX)

Match the existing components (`BookingForm.jsx` is the reference).

- **API access only through `src/api.js`.** Add a named method to the `api` object for every new endpoint;
  components never call `fetch` directly. Paths are relative to `/api` (Vite proxies to :8000).
- Function components with hooks, one component per file in `src/components/`, `export default function Name()`.
- Imports include the `.jsx` / `.js` extension.
- Data loading: `useEffect` + `api.x().then(setX).catch((e) => setError(e.message))`.
- Every screen handles three states: loading (`<p>Loading…</p>`), error (`<p className="error">{error}</p>`), data.
- Show the backend's error message as-is (`err.message` already contains the API `detail`); do not invent messages.
- Forms: controlled inputs with a single `form` state object and an `update` handler keyed by `name`;
  field names match the API's snake_case fields.
- Routes are declared only in `App.jsx`; navigation links use `NavLink`.
- Styling: reuse the classes in `src/index.css` (`container`, `form`, `button`, `error`, …). No CSS frameworks.
- Formatting: 2-space indent, single quotes, no semicolons.
- No new npm dependency without asking; the project targets Node 16.

## Verify

```bash
make frontend-build
```

The build must succeed. For behaviour, the backend specs (`make test`) are the source of truth.
