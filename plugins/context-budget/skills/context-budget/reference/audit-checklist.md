# Audit Checklist: the /context-audit procedure (reference)

The step-by-step routine `/context-audit` runs, in checklist form. Load on demand.

The goal of an audit is a **lean always-loaded tier** with **no loss of
decision-relevant information**. You measure what's resident, apply one keep-vs-cut
test to every section, and relocate what fails the test to the tier where it pays
for itself.

---

## Step 1 — Inventory what's resident

List every file that loads on every turn and estimate its weight:

- [ ] Repo-root `CLAUDE.md`.
- [ ] Any nested `CLAUDE.md` in subdirectories (each adds resident cost when in scope).
- [ ] User-global `~/.claude/CLAUDE.md`, if in scope.
- [ ] Each `SKILL.md` (only name+description is resident, but flag oversized bodies).
- [ ] MCP servers configured — are their tool schemas resident or deferred?

Estimate tokens as `words / 0.75` (≈ 1.33 tokens/word; code and tables run
higher). The bundled `scripts/estimate-context.sh` gives a fast per-file number.
Label every figure an **estimate**; prefer the live `/context` readout where
available.

## Step 2 — Score every section with ONE test

For each section of each memory file, apply the keep-vs-cut test:

> **"Would removing this cause Claude to make a mistake it otherwise wouldn't?
> If not, cut it."**

Three quick disqualifiers make the answer "cut":

- [ ] **Derivable?** Can Claude get it by reading the repo (files, `package.json`,
      configs, CI, Makefile)? → CUT; derive live so it never goes stale.
- [ ] **Generic?** Does a competent model already know it (language idioms,
      framework basics, SOLID/DRY, git workflow)? → CUT.
- [ ] **Situational?** Needed only on *some* tasks or *some* paths, not every
      turn? → don't preload; MOVE it (see Step 4).

Only content that is **non-derivable, non-generic, and broadly relevant** survives
as resident memory. In practice that's: non-obvious gotchas, safety/destructive-
action guardrails, project-specific conventions that can't be inferred, and
one-line pointers to skills.

## Step 3 — Check the skills themselves

- [ ] Any `SKILL.md` over **~2,000 tokens**? Extract heavy sections into
      `reference/*.md` it links to and reads on demand.
- [ ] Is each `description` a sharp **trigger + keywords**? That string is the
      *only* thing routing sees — vague descriptions either never fire or fire on
      everything. Rewrite weak ones.
- [ ] Any content duplicated across a skill and CLAUDE.md, or across nested
      CLAUDE.md files? Keep one source, point to it from the other.

## Step 4 — Relocate what failed the test

Move each cut/situational block to the tier where it costs nothing until relevant:

- [ ] **Procedures / how-tos / workflows → a skill.** Anything shaped like "when
      doing X, do Y" (deploy steps, release checklist, a multi-step task). It
      loads only when its description matches. Give it a precise trigger.
- [ ] **Directory- or file-type-specific guidance → path-scoped
      `.claude/rules/*.md`.** Route conventions, per-layer patterns, test rules.
      These attach only when Claude touches a matching path, so they're dormant
      while you work elsewhere. (E.g. `src/api/` route rules, `test/` mocking rules.)
- [ ] **Deep reference detail → `reference/*.md` under a skill.** Tables,
      matrices, long worked examples — loaded only on explicit read.
- [ ] **Derivable content → nowhere.** Don't relocate a dir tree or dep list;
      delete it and let Claude read the repo when it needs the current truth.
- [ ] **MCP tool schemas → deferred.** Prefer name-only listings with schemas
      fetched on demand over resident full schemas.

## Step 5 — Report and confirm before changing anything

Produce, per file:

- [ ] Estimated **current** resident tokens → estimated **post-trim** resident tokens.
- [ ] A **KEEP/CUT table**: `Section | Decision | Reason | Destination`.
- [ ] The concrete restructure plan (lean CLAUDE.md text + which skills/rules to create).
- [ ] Offer to apply it — but **never delete content without showing the diff and
      asking first**. Show the before/after so the user sees exactly what moves where.

---

## The keep-vs-cut test, applied (quick reference)

| Section | Remove it → mistake? | Decision | Destination |
|---|---|---|---|
| Directory tree / file listing | No — Claude can glob | CUT | derive live |
| Dependency list | No — it's in the manifest | CUT | manifest |
| Standard build/test/lint commands | No — in `package.json`/CI | CUT | derive, or a skill |
| Generic best-practice essay | No — model knows it | CUT | delete |
| Deploy / release procedure | Only when deploying | MOVE | a `deploy` skill |
| Per-directory conventions | Only under that path | MOVE | `.claude/rules/*.md` |
| "Auth service caches 5m silently" | **Yes** | KEEP | CLAUDE.md |
| "Never migrate against prod" | **Yes** (safety) | KEEP | CLAUDE.md |
| "Money in integer cents" | **Yes** | KEEP | CLAUDE.md |
| Skill pointer ("for X use the `foo` skill") | enables disclosure | KEEP | CLAUDE.md |

If in doubt, run the one test: *would removing it cause a mistake?* If the honest
answer is no, it isn't earning its resident cost — cut or move it.
