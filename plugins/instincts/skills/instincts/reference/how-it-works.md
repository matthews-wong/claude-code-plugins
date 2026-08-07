# How instincts work

Instincts implement a simple continuous-learning loop: raw experience becomes
notes, recurring notes become durable rules, and those rules are surfaced every
session so the agent follows them automatically.

## The loop

```
observe -> note (knowledge-loop) -> promote -> instinct -> surface each session -> agent follows
                                       ^                                              |
                                       +----------------- recurs --------------------+
```

1. **Memory (raw learnings).** The sibling `knowledge-loop` plugin captures
   folder-scoped notes as they happen: gotchas, corrections, conventions. These
   are low-friction and noisy by design.
2. **Learning (promotion).** `instincts.py promote` scans those notes,
   clusters them by token overlap, and graduates a rule when a lesson **recurs**
   (a cluster of `--min-support` or more notes) or when a note is explicitly
   marked `kind: semantic` (already a distilled fact). This is the step that
   turns a repeated lesson into a durable rule.
3. **Instinct (durable rule).** The promoted rule lives in
   `.claude/instincts/instincts.jsonl` with a confidence and support count.
4. **Surfacing.** A SessionStart hook runs `surface.sh`, which prints the top
   active instincts for the global scope and the current folder. The agent sees
   them at the start of every session and follows them.

## Confidence and support model

Each instinct tracks a `support` integer (times reinforced) and a derived
`confidence` in the open interval (0, 1):

```
confidence = 1 - 0.5 ** support
```

| support | confidence |
|---------|-----------|
| 1       | 0.50      |
| 2       | 0.75      |
| 3       | 0.875     |
| 4       | 0.9375    |
| 5       | 0.969     |

A fresh rule starts modest (0.50). Every reinforcement roughly halves the
remaining doubt, so repeatedly observed rules climb toward — but never reach —
1.0. Listing and surfacing sort by scope relevance first, then by confidence,
so the strongest, most-relevant rules lead.

## Deduplication and reinforcement

When adding, importing, or promoting, a new rule is compared against existing
rules **in the same scope** using Jaccard token overlap (stopwords removed). If
the overlap is at least `0.8`, the existing instinct is **reinforced** —
`support += 1`, confidence recomputed, tags merged, `updated` refreshed —
instead of creating a duplicate. This is why saying the same thing twice makes a
rule stronger rather than cluttering the store.

## Export / import for cross-project sharing

Instincts are portable. `export` writes every instinct to a single JSON file;
`import` merges such a file into another project's store using the same
dedup/reinforce rule. This lets you carry hard-won rules from one repo to
another, share them with a teammate, or back them up — without dragging along
the raw, folder-specific notes they came from.

## How it pairs with knowledge-loop

`knowledge-loop` and `instincts` are two layers of the same memory system:

- **knowledge-loop** = raw, folder-scoped notes. High volume, low confidence,
  captured cheaply as work happens.
- **instincts** = distilled, high-confidence rules. Low volume, promoted only
  when a lesson recurs, surfaced every session.

`instincts` reads knowledge-loop's store during `promote` but never writes to
it; the two plugins are independent and each works without the other. If
knowledge-loop is not installed, you can still add instincts by hand — promotion
simply finds nothing to graduate and exits cleanly.
