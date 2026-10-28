# Stack playbooks

Read only the section matching the project. These are defaults; user overrides win.

## Frontend (React/Next/Vite)
- Next.js App Router for sites needing SSR/SEO or full-stack; Vite + React for SPAs.
- TypeScript strict, Tailwind CSS, Zustand for client state, TanStack Query for server state.
- Structure: `src/app` or `src/pages`, `src/components`, `src/features/<name>`, `src/lib`, `src/hooks`, `src/store`, `src/types`.
- Ship: error boundary, loading skeletons, empty states, keyboard-accessible controls, responsive layout.
- Tests: Vitest + Testing Library for components and utilities.

## Backend (Python)
- FastAPI for new APIs; Django + DRF when admin, ORM and auth batteries matter.
- Structure: `app/main.py`, `app/api/routers`, `app/services`, `app/models`, `app/schemas`, `app/core/config.py`, `app/db`, `tests/`.
- Pydantic settings from env, structured logging, global exception handlers, health endpoint, migrations (Alembic or Django).
- Tests: pytest with a test client and an isolated test database.

## Backend (Node/TypeScript)
- Fastify or Hono for lean APIs; NestJS when the user wants heavy structure.
- Zod validation, Prisma or Drizzle for the database, pino logging, Vitest.

## Full-stack monorepo
- Layout: `apps/web`, `apps/api` (or `frontend/`, `backend/`), optional `packages/shared`.
- pnpm workspaces when the JS side has multiple packages. Document one command to run everything (e.g. root `pnpm dev` or `docker compose up`).
- Define the API contract once (OpenAPI or shared Zod/TS types) and wire CORS and base URLs through env.

## ML / AI
- Structure: `src/<pkg>/data`, `models`, `train.py`, `evaluate.py`, `inference.py`, `serve.py`, `configs/`, `tests/`, `notebooks/` only if requested.
- Seed everything, version configs, log metrics, keep model artifacts out of git (`.gitignore` plus a note on where to fetch or train).
- LLM apps: isolate prompts in their own module, add retries and timeouts, never log secrets.

## CLI
- Python: Typer or Click. Node: commander. Go: cobra. Rust: clap.
- Document every command in the README, return meaningful exit codes, support `--help` and `--version`.

## Libraries / packages
- Public API in one entry module, semantic versioning, typed exports, changelog, usage examples in the README, publishing config (`pyproject.toml` build backend or `package.json` exports).
