# gp-frontend: notes for Claude

The Angular web app for the Concept Development GP. A user drops a pin on a map, watches the
research run live in a chat, answers the expert's questions, reads results as cards with a
source behind every claim, and edits results to rerun what depends on them.

It talks to `gp-backend` over REST (start a concept, read results, answer escalations, edit
fields) and a WebSocket (live progress).

## Read before any task

1. **The SDLC documents** live in gp-backend: `docs/sdlc/<phase>/intent.md`, `spec.md` and
   `plan.md`. Frontend tasks are the `E…` tasks in the plan. Build exactly the task you're on,
   to its "done when", and put the task ID in the PR title.
2. **The ui-craft skill, for all UI work:** every screen, component, style or UI review. It
   sets the brand direction, tokens (spacing, sizing, type, color, contrast), states, motion,
   accessibility and the final gates.
3. **The GP design system:** once a direction is chosen (plan task E1), its tokens live in
   `src/styles/`. Use only those tokens; never raw hex, px or ms in components.

Don't invent screens, layouts or copy that the spec or the project lead hasn't given. Ask.

## Commands

```bash
npm ci                   # install
npm start                # http://localhost:4200
npm run generate:types   # regenerate types after a schemas submodule bump
npm run typecheck        # strict type check
npm run lint             # ESLint
npm run format           # Prettier (CI runs format:check)
npm test -- --watch=false
npm run build
python3 scripts/lint_ui.py src/                    # ui-craft lint
python3 scripts/contrast.py "#1a1a1a:#ffffff:text" # WCAG contrast for token pairs
```

## Rules that matter most

- **Types come from gp-schemas.** Use the generated types in `src/app/shared/schemas/`; never
  hand-write an API type, and never edit the generated files.
- **Every claim shown to the user links to its source** (the `evidence` on each fact). A card
  never shows a number without one.
- **Progress names:** `progress_phase`, `progress_status`, `progress_step`, `progress_percent`,
  `progress_agent`. Never a bare `step` or `status`.
- **Map:** Google Maps through `@angular/google-maps`, with satellite view. The API key is
  restricted and comes from the environment config, never committed.
- **Accessibility:** WCAG 2.2 AA (see ui-craft). Use the Angular CDK for focus traps, live
  announcements and keyboard lists.
- **Every state exists:** loading, empty, error, waiting for the expert, rerunning.

## Git and PRs

- Branch from `develop`: `feature/<clickup-id>-short-name` or `fix/<clickup-id>-short-name`.
- One plan task per PR, into `develop`. Only the project lead merges.
- Fill in the PR template. "Why" explains each choice and the alternative not chosen.

## Explaining your work

The team wants to understand every change, not just receive it. When you finish a task,
explain **what** you changed, **why** this way and not another, and **how** it works, in plain
language. Explain any new term the first time it appears.

## Hooks in this repo (`.claude/settings.json`)

| Hook | What it does |
|---|---|
| Before an edit | Blocks edits to `src/app/shared/schemas/`, `schemas/` and `.env` files |
| Before a shell command | Blocks pushing to `main`/`develop`, force pushes, and committing while on `main`/`develop` |
| After an edit | Runs Prettier on the file, then the ui-craft lint; any findings come back to Claude to fix or justify |
| Before finishing | Runs the type check and ESLint if `src/` changed; failures send Claude back to fix them |

If a hook blocks you, read its message and follow it. Don't work around it.
