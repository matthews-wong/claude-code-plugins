# Credits & inspiration

This marketplace is original work (MIT © 2026 Matthews Wong), but good open source
builds on good open source. These projects and writings shaped the *ideas* here —
none of their code was copied; where a concept is borrowed it was re-implemented
from scratch in this repo's own style.

## Memory & continuous learning
- **ECC — "Everything Claude Code"** by Affaan Mustafa (MIT). Inspired the
  `instincts` plugin's concept of promoting recurring lessons into durable,
  auto-surfaced rules, and reinforced the "memory + continuous learning" direction
  of `knowledge-loop`. Clean-room implementation — no code reused.
  https://github.com/affaan-m/ECC
- Agent-memory research that shaped `knowledge-loop`'s retrieval design:
  **Reflexion** (reflective episodic memory), **Mem0** and **A-Mem** (extract →
  consolidate → retrieve; dedup; decay), and the standard **reciprocal rank fusion**
  and **recency-decay** retrieval patterns.

## Claude Code practice
- **Boris Cherny** and the official **Claude Code best-practices** guide — the
  agentic-adoption core, verification-first workflow, and lean-context principles
  (see [`docs/boris-cherny-principles.md`](./docs/boris-cherny-principles.md)).

## A note on provenance
Everything here is intended to stand on its own merits. If you recognize an idea
from your project and feel it deserves clearer attribution, open an issue — happy
to credit it.
