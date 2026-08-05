---
name: token-budget
description: Use when a session feels heavy, slow, or near its context limit, or before deciding to /compact or /clear — summarizes what is filling the context window (from /context) and gives prioritized, concrete steps to trim it and stay within budget.
---

You are producing a token-budget summary for the current session. The goal is to
help the user understand what is consuming their context window and where to trim
it, so the session stays economical and responsive.

1. Point the user to the ground truth. The authoritative, live view of context
   usage is Claude Code's built-in `/context` command — tell the user to run it
   (or reference its most recent output) for the exact token breakdown by
   category (system prompt, tools, messages, files, MCP servers, memory). Do not
   fabricate specific token numbers you cannot observe; work from what `/context`
   reports and from what is visible in this conversation.

2. Summarize, in plain language, what is likely occupying the window right now:
   - Long files read in full that only needed a slice.
   - Large tool outputs (build logs, test dumps, big search results) left in the
     transcript.
   - MCP servers whose tool definitions add fixed overhead every turn.
   - Accumulated back-and-forth from a task that is already finished.

3. Give concrete, prioritized trimming suggestions, biggest wins first:
   - `/clear` to reset context when starting an unrelated task.
   - `/compact` (optionally with focus instructions) to condense a long session
     while keeping the thread of the current task.
   - Re-read only the needed ranges of large files instead of whole files.
   - Delegate sprawling searches or log-scraping to a subagent so the bulk output
     stays out of the main context and only the conclusion returns.
   - Disable MCP servers not needed for the current task to shed their per-turn
     tool-definition overhead.
   - Prefer targeted tools over dumping large command output into the transcript.

4. Close with a one-line budget posture: whether the session looks lean, getting
   heavy, or near a point where compacting is worthwhile — based on `/context`
   output and the visible conversation, not invented figures.

Keep it short and actionable. This command is about awareness and hygiene, not
precise accounting.
