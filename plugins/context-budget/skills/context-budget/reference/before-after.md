# Before / After: slimming a bloated CLAUDE.md (reference)

A concrete, worked transformation. Load on demand.

The BEFORE is a ~200-line `CLAUDE.md` typical of a project that dumped everything
into always-loaded memory. The AFTER is a ~40-line lean core that keeps only what
Claude cannot derive, with everything else relocated to skills and path-scoped
rules. Every turn pays for the whole file, so this is a direct budget win on every
single message.

---

## BEFORE — `CLAUDE.md` (~200 lines, ~2600 est. tokens, loaded every turn)

```md
# Acme Payments Service

## Project Overview
Acme Payments is a Node.js service that processes payments. It exposes a REST API
and talks to Postgres and Stripe. It is written in TypeScript and uses Express.
The team follows agile and ships weekly. This document describes everything you
need to know to work on the codebase.

## Tech Stack
- Node.js 18
- TypeScript 5
- Express 4
- Postgres 15 (via node-postgres / pg)
- Redis 7 (rate limiting + cache)
- Stripe SDK
- Zod for validation
- Jest for tests
- ESLint + Prettier
- Docker + docker-compose for local dev

## Directory Structure
- src/
  - index.ts            — app entry point
  - server.ts           — Express bootstrap
  - config/             — env + config loading
  - api/
    - routes/           — route handlers
    - middleware/        — auth, logging, error handling
  - db/
    - models/           — data models
    - migrations/        — SQL migrations
    - client.ts          — pg pool
  - services/
    - payments/          — payment orchestration
    - stripe/            — Stripe wrapper
    - notifications/     — email + webhook senders
  - lib/                 — shared utilities
  - types/               — shared TypeScript types
- test/                  — Jest tests mirroring src/
- scripts/               — one-off maintenance scripts
- docker-compose.yml
- package.json
... (30+ more lines enumerating files) ...

## Dependencies
express@4, pg@8, ioredis@5, stripe@14, zod@3, pino@8, dotenv@16,
jsonwebtoken@9, date-fns@3, uuid@9 ...
Dev: jest@29, ts-jest, eslint, prettier, @types/*, supertest ...
(20+ lines listing every dependency and version)

## Getting Started
1. Clone the repo.
2. Run `npm install`.
3. Copy `.env.example` to `.env`.
4. Run `docker-compose up -d` to start Postgres and Redis.
5. Run `npm run migrate` to set up the schema.
6. Run `npm run dev` to start the dev server on port 3000.

## Commands
- `npm run dev` — start the dev server with hot reload
- `npm run build` — compile TypeScript to dist/
- `npm test` — run the Jest suite
- `npm run test:watch` — Jest in watch mode
- `npm run lint` — run ESLint
- `npm run format` — run Prettier
- `npm run migrate` — apply DB migrations
- `npm run seed` — seed local data

## Coding Standards
- Write clean, readable code. Follow SOLID principles.
- Use meaningful variable names.
- Keep functions small and focused; one responsibility each.
- Prefer composition over inheritance.
- Don't repeat yourself (DRY).
- Handle errors properly and don't swallow exceptions.
- Write tests for new features.
- Use async/await instead of raw promises where possible.
- Comment complex logic.
- Follow the existing code style.
(20+ lines of generic best-practice advice)

## Git Workflow
- Create a feature branch off main.
- Make small, atomic commits.
- Write descriptive commit messages.
- Open a PR and request review.
- Squash-merge once approved.
- Delete the branch after merge.

## API Conventions
- All routes live under src/api/routes.
- Use Zod schemas to validate request bodies.
- Return JSON. Use standard HTTP status codes.
- Wrap handlers so errors reach the error middleware.

## Testing
- Tests live in test/, mirroring src/.
- Run npm test. Aim for good coverage.
- Use supertest for API tests.
- Mock Stripe in unit tests.

## Deployment
- CI runs on GitHub Actions (see .github/workflows/ci.yml).
- Merges to main deploy to staging automatically.
- Promote to prod via the "Deploy" workflow_dispatch.

## Gotchas
- The rate limiter uses ONE shared Redis key. Running two dev servers against the
  same Redis double-counts and can lock you out. Set REDIS_PREFIX per instance.
- All monetary amounts are stored as integer cents. NEVER use floats for money.
- Stripe webhooks must be verified with the raw request body — our JSON body
  parser is disabled on the /webhooks route for exactly this reason. Don't add
  express.json() back to that route.
- migrations are irreversible in prod; there is no down-migration runner wired up.
- The staging DB is a shared instance; never run destructive scripts against it.
```

### What's wrong with the BEFORE

Almost all of it is **derivable** or **generic** — content Claude can reconstruct
from the repo on demand or already knows:

| Section | Verdict | Why |
|---|---|---|
| Project Overview | CUT | Prose narration; inferable from the repo and README. |
| Tech Stack | CUT | It's in `package.json`. |
| Directory Structure | CUT | Claude can `ls`/glob the tree live. |
| Dependencies | CUT | Verbatim from `package.json` — and goes stale instantly. |
| Getting Started | CUT | Standard onboarding; belongs in README, not per-turn memory. |
| Commands | CUT | In `package.json` `scripts`; discoverable. |
| Coding Standards | CUT | Generic best practices the model already applies. |
| Git Workflow | CUT | Generic; not project-specific. |
| API Conventions | MOVE | Only relevant when touching routes → path-scoped rule. |
| Testing | MOVE/CUT | Mostly generic; the one real rule (mock Stripe) → test rule. |
| Deployment | MOVE | Only relevant when deploying → a `deploy` skill. |
| Gotchas | **KEEP** | Non-obvious, safety-critical, not visible in code. |

Only the Gotchas earn always-loaded status. Everything above them is paid for on
every turn while being relevant on almost none of them.

---

## AFTER — `CLAUDE.md` (~40 lines, ~350 est. tokens, loaded every turn)

```md
# Acme Payments Service

Node/TS payment service (Express + Postgres + Redis + Stripe). Stack, structure,
deps, and scripts are all discoverable from the repo — read them when you need
them rather than trusting a snapshot here.

## Gotchas (non-obvious — read before editing)
- **Rate limiter shares ONE Redis key.** Two dev servers against the same Redis
  double-count and can lock you out. Set `REDIS_PREFIX` per instance.
- **Money is integer cents everywhere.** Never introduce floats for monetary
  amounts.
- **Stripe webhooks need the raw body.** `express.json()` is deliberately OFF on
  `/webhooks` so signatures verify. Do not re-add a JSON parser to that route.

## Safety
- Migrations are **irreversible in prod** (no down-runner). Confirm before applying.
- The **staging DB is shared** — never run destructive scripts against it.

## Where the depth lives
- Deploying / promoting to prod → the **`deploy` skill**.
- API route conventions → `.claude/rules/api-routes.md` (auto-applies under `src/api/`).
- Test conventions (e.g. mock Stripe) → `.claude/rules/tests.md` (applies under `test/`).
```

### The moves that made it lean

1. **Deleted (derivable):** Overview, Tech Stack, Directory Structure,
   Dependencies, Getting Started, Commands, Coding Standards, Git Workflow. None
   of it prevents a mistake — Claude gets the truth from the repo, always current.

2. **Deployment → a skill.** `deploy` loads only its name+description until a
   deploy task fires, then its `SKILL.md` carries the staging/prod procedure. Zero
   resident cost the other 99% of the time.

3. **API + testing conventions → path-scoped `.claude/rules/*.md`.** These attach
   only when Claude touches matching files, so route rules aren't resident while
   you edit the DB layer, and vice-versa.

4. **Kept the irreducible core:** the four real gotchas and the two safety rules —
   the only content whose removal would cause real, non-obvious mistakes.

---

## The transformation as a diff

```diff
  # Acme Payments Service

- ## Project Overview
- Acme Payments is a Node.js service that processes payments...
-
- ## Tech Stack
- - Node.js 18
- - TypeScript 5
- ... (whole stack list) ...
-
- ## Directory Structure
- - src/
-   - index.ts ...
- ... (40+ lines of tree) ...
-
- ## Dependencies
- express@4, pg@8, ioredis@5 ... (20+ lines)
-
- ## Getting Started
- 1. Clone the repo. 2. npm install ...
-
- ## Commands
- - npm run dev ...  (all scripts, verbatim from package.json)
-
- ## Coding Standards
- - Write clean, readable code. Follow SOLID ... (20+ generic lines)
-
- ## Git Workflow
- - Create a feature branch off main ...
-
- ## API Conventions
- - All routes live under src/api/routes ...
+ Node/TS payment service (Express + Postgres + Redis + Stripe). Stack, structure,
+ deps, and scripts are all discoverable from the repo — read them when you need them.

- ## Deployment
- - CI runs on GitHub Actions ...
- - Merges to main deploy to staging ...
+ ## Where the depth lives
+ - Deploying / promoting to prod → the `deploy` skill.
+ - API route conventions → .claude/rules/api-routes.md (applies under src/api/).
+ - Test conventions → .claude/rules/tests.md (applies under test/).

  ## Gotchas
  - Rate limiter shares ONE Redis key ...
  - Money is integer cents everywhere ...
  - Stripe webhooks need the raw body ...
+ ## Safety
+ - Migrations are irreversible in prod ...
+ - Staging DB is shared — no destructive scripts ...
```

Net: **~2600 → ~350 est. tokens** always-loaded (roughly an **85% cut**), with
**zero loss of decision-relevant information** — the derivable content is now
fetched live and the situational content loads only when its task or file is in
play.
