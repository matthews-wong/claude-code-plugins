#!/usr/bin/env python3
"""Append a learning note to the local, folder-scoped knowledge store.

Writes one JSON object per line to .claude/knowledge/notes.jsonl under the project
root (CLAUDE_PROJECT_DIR if set, else cwd). Creates the directory and file if
missing, assigns a unique id and an ISO-8601 timestamp.

Pure Python 3, standard library only.

Usage:
    store.py --text "the lesson" [--folder "relative/path"] [--tags "a,b,c"]
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime


def project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def rel_folder(root, raw):
    """Normalise a folder to a project-relative, POSIX-style path (default: cwd)."""
    if not raw:
        try:
            raw = os.path.relpath(os.getcwd(), root)
        except ValueError:
            raw = "."
    raw = raw.strip()
    if os.path.isabs(raw):
        try:
            raw = os.path.relpath(raw, root)
        except ValueError:
            raw = os.path.basename(raw.rstrip("/\\"))
    raw = raw.replace("\\", "/").strip("/")
    return raw or "."


def parse_tags(raw):
    if not raw:
        return []
    # Accept comma- or whitespace-separated tags.
    parts = [t.strip() for chunk in raw.split(",") for t in chunk.split()]
    return [t for t in parts if t]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Append a learning note to the folder-scoped knowledge store."
    )
    parser.add_argument("--text", required=True, help="The lesson (self-contained).")
    parser.add_argument("--folder", default="", help="Project-relative folder scope.")
    parser.add_argument("--tags", default="", help="Comma/space-separated tags.")
    args = parser.parse_args(argv)

    text = args.text.strip()
    if not text:
        sys.stderr.write("store.py: --text must not be empty\n")
        return 1

    root = project_dir()
    folder = rel_folder(root, args.folder)
    tags = parse_tags(args.tags)

    note = {
        "id": uuid.uuid4().hex[:12],
        "text": text,
        "folder": folder,
        "tags": tags,
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    store_dir = os.path.join(root, ".claude", "knowledge")
    store_file = os.path.join(store_dir, "notes.jsonl")
    try:
        os.makedirs(store_dir, exist_ok=True)
        with open(store_file, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(note, ensure_ascii=False) + "\n")
    except (OSError, IOError) as exc:
        sys.stderr.write("store.py: could not write store: {}\n".format(exc))
        return 1

    print("Stored learning {} in {} (folder: {})".format(note["id"], store_file, folder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
