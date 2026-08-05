#!/bin/sh
# token-report.sh — non-blocking session token-budget reminder.
#
# Runs on SessionStart via the token-budget-tracker plugin hook. It prints a
# short, friendly nudge to stay aware of the session's token budget and to use
# /context to inspect what is occupying the context window. It performs no
# network calls, mutates nothing, and always exits 0 so it can never block or
# interrupt a session.

# Optional override: set TOKEN_BUDGET_HINT in the environment to show your own
# target (e.g. "aim to stay under 100k before compacting").
HINT="${TOKEN_BUDGET_HINT:-keep an eye on context growth and compact or /clear when a task is done}"

printf '%s\n' "[token-budget-tracker] Session started."
printf '%s\n' "  - Run /context to see what is filling the context window."
printf '%s\n' "  - Run /token-budget for a usage summary and trimming suggestions."
printf '%s\n' "  - Budget note: ${HINT}."

# Never block the session, whatever happened above.
exit 0
