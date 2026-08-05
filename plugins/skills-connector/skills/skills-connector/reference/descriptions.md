# Writing a description that fires

**A vague description is the #1 reason a skill fails to fire.** Claude routes to a skill by
reading its frontmatter `description` and nothing else. If that one sentence does not make
the trigger situation obvious, the skill sits unused no matter how good its body is.

The description is a **trigger, not a title.** It must answer two things:

1. **What** the skill does.
2. **When** to use it — the tasks, verbs, file types, error messages, and phrasings a user
   would actually say, in their vocabulary.

## The recipe

- **Lead with the trigger:** start with `Use when …`.
- **Name concrete cues:** the file extensions, tools, verbs, and symptoms that should fire
  it (`.tf` files, "flaky test", "rebase", "429", "webhook").
- **Scope it:** specific enough not to over-trigger, broad enough to catch real phrasings.
- **Third person about the situation**, not first person about yourself. Describe the user's
  task, not "I can help you…".

## BAD vs GOOD

| BAD (vague — under-fires) | GOOD ("Use when…" + concrete keywords) |
|---|---|
| `Helps with databases.` | `Use when writing, reviewing, or optimizing Postgres SQL or schema migrations — indexing, query plans, safe migration ordering, and online (lock-free) DDL.` |
| `Git utilities.` | `Use when writing a git commit message or fixing a rejected one — enforces Conventional Commits (type(scope): summary), imperative mood, and a 50-char subject.` |
| `For testing.` | `Use when a test is flaky, slow, or failing intermittently — diagnoses timing/order/shared-state causes and rewrites the test to be deterministic.` |
| `Handles API stuff.` | `Use when calling or debugging a REST/GraphQL client — retries, backoff on 429/5xx, pagination, and auth-token refresh.` |
| `Documentation helper.` | `Use when writing or updating a README or module docstring — covers structure, a runnable quickstart, and keeping examples in sync with the code.` |
| `Makes code better.` | `Use when refactoring for readability — extracting functions, naming, removing dead code — without changing behavior or public signatures.` |
| `Terraform things.` | `Use when authoring or reviewing Terraform (.tf) for AWS — module structure, state/locking safety, and plan review before apply.` |

## Why the BAD column fails

- **No "when".** "Helps with databases" describes a topic, not a trigger. Claude cannot tell
  whether the current task is one of them.
- **No keywords to match.** With no verbs or file types, nothing in a real user message
  lines up with the description.
- **Too broad, so it never wins.** A description that could apply to anything competes with
  everything and routes to nothing reliably.

## Quick self-test

Read your description and ask: *"If a user typed a task this skill should handle, would the
words they'd use appear here?"* If not, add those words. Then check the reverse — that it
would **not** fire on adjacent tasks it shouldn't own (that is the job of scoping and of
splitting; see the main SKILL.md).
