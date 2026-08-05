#!/usr/bin/env sh
# =============================================================================
# fan-out.sh — TEMPLATE for fanning a repetitive change out across many files.
#
# Practice: "Fan out across files" from Anthropic's Claude Code best practices.
# It loops a scoped, headless `claude -p` invocation over a list of files so a
# large mechanical migration runs one small task per file instead of one giant
# conversation.
#
# ---------------------------------------------------------------------------
# THIS IS A TEMPLATE. Read it, edit the marked spots, prove it on 2-3 files,
# THEN enable the live run. It is NON-DESTRUCTIVE by default: as shipped it
# only PRINTS the command it would run for each file (a dry run). Nothing is
# edited or committed until you uncomment the live invocation below.
# ---------------------------------------------------------------------------
#
# Workflow:
#   1. Build files.txt: one target file path per line (Glob/Grep the pattern).
#   2. Edit PROMPT below to describe the exact per-file transformation.
#   3. Edit ALLOWED_TOOLS to the least privilege the change needs.
#   4. Start with a SHORT files.txt (2-3 representative files) and run the
#      dry run, then a live run; inspect the diffs.
#   5. When the prompt is reliable, expand files.txt to the full set and run.
#   6. Verify the aggregate afterward (build / tests / git diff).
#
# Usage:
#   sh fan-out.sh              # dry run (default) — prints commands only
#   sh fan-out.sh --live       # actually invoke claude per file
# =============================================================================

set -eu

# --- Configuration -----------------------------------------------------------

# File containing the worklist: one target file path per line.
FILE_LIST="files.txt"

# Tools each headless run is allowed to use. Keep this as tight as possible.
# Example: allow editing the file and committing it, and nothing else.
ALLOWED_TOOLS="Edit,Bash(git commit *)"

# The per-file prompt. $file is substituted per iteration. Be PRECISE: say
# exactly what to change and what to leave alone — ambiguity is multiplied
# across every file in the list. Committing per file keeps changes isolated.
build_prompt() {
  file="$1"
  # -------- EDIT THIS PROMPT for your migration --------
  printf '%s' "Apply the following change to the single file '$file' and nothing else:

  <DESCRIBE THE EXACT TRANSFORMATION HERE>

  Do NOT change unrelated code. Do NOT touch other files.
  If the file does not need the change, make no edits.
  When done and only if you made a change, run:
    git commit -m 'refactor: <describe change> in $file'"
  # -----------------------------------------------------
}

# --- Run mode ----------------------------------------------------------------

LIVE=0
if [ "${1:-}" = "--live" ]; then
  LIVE=1
fi

# --- Preconditions -----------------------------------------------------------

if [ ! -f "$FILE_LIST" ]; then
  echo "error: worklist '$FILE_LIST' not found." >&2
  echo "Create it first: one target file path per line." >&2
  exit 1
fi

if [ "$LIVE" -eq 1 ] && ! command -v claude >/dev/null 2>&1; then
  echo "error: 'claude' CLI not found on PATH (required for --live)." >&2
  exit 1
fi

# --- Loop --------------------------------------------------------------------

count=0
while IFS= read -r file || [ -n "$file" ]; do
  # Skip blank lines and comments (#...).
  case "$file" in
    ''|\#*) continue ;;
  esac

  if [ ! -e "$file" ]; then
    echo "skip: '$file' does not exist" >&2
    continue
  fi

  count=$((count + 1))
  prompt="$(build_prompt "$file")"

  if [ "$LIVE" -eq 1 ]; then
    echo ">>> [$count] processing: $file"
    # -- LIVE invocation. Runs headless, scoped to ALLOWED_TOOLS. --
    claude -p "$prompt" --allowedTools "$ALLOWED_TOOLS"
  else
    # -- DRY RUN (default): show exactly what would run, change nothing. --
    echo ">>> [$count] DRY RUN — would run for: $file"
    echo "    claude -p \"<prompt for $file>\" --allowedTools \"$ALLOWED_TOOLS\""
  fi
done < "$FILE_LIST"

echo
if [ "$LIVE" -eq 1 ]; then
  echo "Done. Processed $count file(s). Now verify the batch: build / tests / git diff."
else
  echo "Dry run complete. $count file(s) in the worklist."
  echo "Prove the prompt on a small files.txt, then re-run with --live."
fi
