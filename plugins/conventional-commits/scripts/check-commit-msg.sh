#!/bin/sh
# check-commit-msg.sh — validate a commit message against Conventional Commits v1.0.0.
#
# Non-blocking by design: this script ALWAYS exits 0. It only emits advisory
# warnings so it never breaks a workflow or a hook chain.
#
# Two modes:
#   1) File/arg mode: pass a path to a commit-message file, or the message on
#      stdin when not invoked as a hook. Example:
#        sh check-commit-msg.sh .git/COMMIT_EDITMSG
#   2) Hook mode (Claude Code PostToolUse on Bash): reads the hook JSON from
#      stdin; if the tool command ran a `git commit`, it validates the message
#      of the most recent commit via `git log -1`.

CONVENTIONAL_REGEX='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9._-]+\))?(!)?: .+'

warn() {
  printf 'conventional-commits: %s\n' "$1" >&2
}

validate_subject() {
  subject="$1"

  # Ignore merge/revert-generated and fixup subjects.
  case "$subject" in
    "Merge "*|"Revert "*|"fixup!"*|"squash!"*)
      exit 0
      ;;
  esac

  if printf '%s' "$subject" | grep -Eq "$CONVENTIONAL_REGEX"; then
    # Subject matches. Add a soft length advisory.
    length=$(printf '%s' "$subject" | wc -c | tr -d ' ')
    if [ "$length" -gt 72 ]; then
      warn "subject is ${length} chars (aim for <= 72): $subject"
    fi
    exit 0
  fi

  warn "message does not follow Conventional Commits: \"$subject\""
  warn "expected: <type>[(scope)][!]: <description>"
  warn "types: feat fix docs style refactor perf test build ci chore revert"
  exit 0
}

# ---- Determine the message to validate ---------------------------------------

# Arg mode: a readable file path was provided.
if [ -n "$1" ] && [ -f "$1" ]; then
  first_line=$(sed -n '1p' "$1")
  [ -n "$first_line" ] && validate_subject "$first_line"
  exit 0
fi

# Read whatever is on stdin (may be empty when run interactively).
input=$(cat 2>/dev/null || true)

# Hook mode: stdin looks like the Claude Code hook JSON payload.
case "$input" in
  *'"tool_name"'*|*'"tool_input"'*)
    # Only act when the executed command was a git commit.
    case "$input" in
      *'git commit'*|*'git'*'commit'*)
        if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
          subject=$(git log -1 --pretty=%s 2>/dev/null)
          [ -n "$subject" ] && validate_subject "$subject"
        fi
        ;;
    esac
    exit 0
    ;;
esac

# Plain stdin mode: treat the first non-empty line as the subject.
first_line=$(printf '%s\n' "$input" | sed -n '1p')
[ -n "$first_line" ] && validate_subject "$first_line"

exit 0
