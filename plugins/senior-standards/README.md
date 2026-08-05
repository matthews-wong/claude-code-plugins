# senior-standards

A Claude Code plugin that encodes the three engineering principles documented at the bottom of Boris Cherny's `CLAUDE.md`, and applies them while coding and reviewing.

The three principles:

1. **Make every change as simple as possible** — minimal code; prefer deleting lines to adding them.
2. **Find the root cause** — no temporary fixes or band-aids; hold to senior-developer standards.
3. **Touch only what's necessary** — no side effects; don't introduce new bugs while fixing old ones.

## Components

- **`skills/senior-standards/SKILL.md`** — a lean skill stating the three principles and how to apply each one while coding and while reviewing.
- **`commands/standards-check.md`** — `/standards-check` reviews your current diff against the three principles and flags concrete violations (band-aid fixes, non-minimal changes, out-of-scope side effects). Review only; it makes no edits.

## Usage

Before committing or opening a PR:

```
/standards-check
```

## Attribution

The three principles are attributed to Boris Cherny's documented `CLAUDE.md`.

## License

MIT © Matthews Wong
