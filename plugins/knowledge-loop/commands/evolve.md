---
name: evolve
description: Use when the knowledge store has accumulated many learnings and you want to turn recurring lessons into a reusable skill. Clusters related notes and drafts a SKILL.md scaffold for each strong cluster, closing the "instincts → skill" continuous-learning loop, then you review and promote the good ones.
---

You are running the **instincts → skill** loop: individual learnings that keep
recurring around the same topic have earned promotion from one-off "instincts"
into a reusable skill. This command drafts those skills; you review and promote.

## 1. Draft the skills

Run the evolve script:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/evolve.py"
```

What it does:

- Clusters the store's notes by TF-IDF cosine similarity (single-link, threshold
  ≥ 0.35) combined with shared folder/tags.
- For each cluster with **≥ 3 notes** and **decent average confidence** (≥ 0.4),
  writes a **DRAFT** `SKILL.md` to `.claude/knowledge/evolved/<slug>/SKILL.md`
  with synthesized frontmatter (`name:` + a routing `description:`) and a body
  listing the clustered lessons.
- Prints a summary of clusters found and drafts written.

Useful flags: `--dry-run` (preview without writing), `--min-size N`,
`--min-confidence F`, `--threshold F`, `--out-dir PATH`.

## 2. Review and promote (your job, not the script's)

The script only **drafts** — it never installs a skill. For each draft written:

1. **Read it.** Open the drafted `SKILL.md` and judge whether the clustered
   lessons really form one coherent, reusable pattern. If a cluster is noise or
   mixes unrelated lessons, discard it.
2. **Sharpen the `description:`** into a strong trigger — the description is what
   makes a skill auto-invoke, so make it say precisely *when* to use the skill
   (the situations, symptoms, and keywords), not just what it contains.
3. **Tighten the body** into actionable guidance: keep the durable lessons, drop
   the trivial, and phrase them as instructions the next agent should follow.
4. **Promote the good ones** by moving the folder into a real skills location — a
   plugin's `skills/` directory or the project's `.claude/skills/` — so it loads
   as a first-class skill. Leave weak drafts in `evolved/` or delete them.

Frame the outcome for the user: recurring instincts have been distilled into
candidate skills; report which you promoted, which you refined, and which you
dropped, and why. This is how the knowledge loop compounds — today's repeated
lessons become tomorrow's automatic behavior.
