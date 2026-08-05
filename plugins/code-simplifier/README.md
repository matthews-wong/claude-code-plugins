# code-simplifier

A Claude Code plugin that simplifies recently-changed code *after* the main work is done — modeled on Boris Cherny's code-simplifier subagent workflow.

Core principle: **if you can delete lines instead of adding them, do that.**

## Components

- **`agents/code-simplifier.md`** — a read-and-edit subagent (Read, Edit, Grep, Glob) that reviews the working diff and makes it simpler without changing behavior: deletes dead code, inlines single-use indirection, removes speculative generality, and flattens control flow.
- **`commands/simplify.md`** — `/simplify` invokes the pass on your current working diff (uncommitted changes, or the files most recently edited).

## Usage

After Claude finishes a feature or fix, run:

```
/simplify
```

The subagent focuses only on the recently-changed code, preserves observable behavior, and prefers removals over additions. If it spots a real bug, it reports it instead of silently fixing it.

## License

MIT © Matthews Wong
