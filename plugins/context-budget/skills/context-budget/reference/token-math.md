# Token Math: the context-budget ledger (reference)

Where context tokens actually go, per strategy. Load on demand.

The point of a budget is that it is finite. Every token that is **resident at
startup** is spent before the task begins and re-spent on every turn. Tokens that
**load on demand** cost nothing until the moment they're relevant, then pay for
themselves. The whole discipline is: move tokens from the first column to the
second without losing decision-relevant information.

Figures below assume a working budget on the order of **200k tokens** and are
**estimates** for illustration — label real numbers as estimates too, and prefer
the actual `/context` readout over any table.

---

## Strategy comparison

| Strategy | Resident at startup | Loads on demand | Est. budget lost while idle | Notes |
|---|---|---|---|---|
| **Dump everything in one big CLAUDE.md** | Whole file, every turn (e.g. ~2,600 tok) | nothing | **~1.3%** and growing per turn | Worst case: pays full price on every message, most of it irrelevant to the current task. |
| **Lean CLAUDE.md + skills** | Lean core (~350 tok) + each skill's name+description (~30–60 tok each) | `SKILL.md` body on trigger; `reference/*.md` on explicit read | **~0.2–0.4%** | The depth exists but is dormant. 10 skills ≈ ~500 resident tokens of metadata total. |
| **Path-scoped `.claude/rules/*.md`** | ~0 until you touch a matching path | rule body when a matching file enters the task | **~0%** while working elsewhere | Route rules aren't resident while you edit the DB layer, and vice-versa. |
| **Subagent (Task/Agent)** | ~0 in the main thread | the subagent gets its OWN budget; only its final report returns | **~0%** in main context | Heavy exploration burns the subagent's window, not yours — you keep the conclusion, not the file dumps. |
| **Deferred MCP tool schemas** | tool NAMES only (a listing) | full JSONSchema fetched via search only when a tool is actually needed | **~0%** for the schemas | A dozen MCP servers' full schemas can be tens of thousands of tokens; deferring keeps them out until called. |

Rule of thumb: the four lower rows all convert *resident* cost into *on-demand*
cost. The top row refuses to, and pays for it continuously.

---

## Why "resident at startup" is the expensive kind

- **It re-bills every turn.** A 2,600-token CLAUDE.md in a 30-turn session isn't
  paid once — it is in the prompt for all 30 turns. Resident tokens are a
  standing tax, not a one-off purchase.
- **It crowds the working set.** Budget spent on dormant memory is budget not
  available for the file you're editing, the test output, the diff. On a long
  task this is the difference between holding the whole picture and thrashing.
- **On-demand tokens are self-justifying.** A `reference/*.md` that loads only
  when the skill reads it is, by construction, relevant at the moment it costs
  anything. Resident memory has no such guarantee — most of it is irrelevant to
  any given turn.

## Worked budget walk

Take a project with 2,600 tokens of CLAUDE.md, 10 skills, 3 path rules, and 3 MCP
servers whose full schemas total ~18,000 tokens.

- **All-resident approach:** 2,600 (memory) + 18,000 (MCP schemas) ≈ **20,600
  tokens resident every turn** ≈ ~10% of a 200k budget gone before the task
  starts — most of it never used on any single turn.
- **Budgeted approach:** ~350 (lean memory) + ~500 (10 skills' metadata) + ~0
  (rules dormant) + tool *names* only for MCP ≈ **~1,000–1,500 tokens resident**,
  with the other ~19k available on demand. Roughly a **13–20x** reduction in
  standing cost, and the deferred depth is still one trigger away.

---

## Why routing degrades as context fills

Slimming isn't only about free space — it protects **decision quality**:

- **Routing is a matching problem.** When Claude decides whether to invoke a skill
  or a tool, it matches the task against the descriptions in context. More
  always-on, mostly-irrelevant text is more distractors to match against, which
  blurs attention and weakens selection. A lean context has a higher
  signal-to-noise ratio, so the right skill fires more reliably.
- **Attention thins as the window fills.** As total occupied context grows,
  relevant instructions get "diluted" among far more tokens. Guidance that was
  followed reliably at 10% fill can be skipped or half-applied at 80% fill — not
  because it changed, but because it's now competing with much more material.
- **Compounding failure mode.** Bloat causes earlier auto-compaction; compaction
  can drop or summarize away the very gotcha you needed; the model then makes the
  mistake the gotcha was meant to prevent. Keeping resident context lean pushes
  that cliff further out and keeps the load-bearing rules sharp.

The takeaway: resident tokens cost you **twice** — raw budget *and* routing
fidelity — so every token you can push to on-demand loading buys back both.
