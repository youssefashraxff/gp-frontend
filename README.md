# gp-frontend

Angular web app for the Concept Development GP: clients start a concept from a site location, watch progress live, and the expert answers escalations.

Talks to `gp-backend` over REST (start a concept, read results) and WebSocket (live progress).

## Getting started

```bash
git clone --recurse-submodules <repo-url>
cd gp-frontend
npm ci
npm start            # http://localhost:4200
```

Already cloned without submodules? `git submodule update --init`.
After every pull: `git submodule update` (keeps `schemas/` on the pinned commit).

## Shared types

Request/response shapes come from `gp-schemas` (submodule at `schemas/`):

```bash
npm run generate:types   # writes src/app/shared/schemas/
```
Never edit `src/app/shared/schemas/` by hand. Commit regenerated types together with any submodule bump — CI fails if they don't match.

## Checks (same as CI)

```bash
npm run lint
npm run format:check
npm run typecheck
npm test -- --watch=false
npm run build
```

## Workflow

- `main` = production, `develop` = integration. Branch from `develop`, PR back into `develop`.
- Branch names: `feature/<clickup-id>-short-name`, `fix/<clickup-id>-short-name`.
- Every PR is reviewed by Youssef. Done = merged into `develop`.
