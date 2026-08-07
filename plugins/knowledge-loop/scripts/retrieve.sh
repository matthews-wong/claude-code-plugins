#!/bin/sh
# SessionStart hook: surface relevant prior learnings for the current folder.
# Non-blocking by contract — tolerate a missing python and always exit 0 so a
# retrieval failure can never interrupt or delay the session.
if command -v python3 >/dev/null 2>&1; then
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieve.py" "$(pwd)" 2>/dev/null
fi
exit 0
