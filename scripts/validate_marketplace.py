#!/usr/bin/env python3
"""Validate the plugin marketplace.

Checks, for the marketplace in this repo:
  - marketplace.json parses and has the required fields
  - every plugin entry resolves to a directory with a valid .claude-plugin/plugin.json
  - each plugin.json 'name' matches its marketplace entry
  - no duplicate plugin names
  - every hooks.json parses as valid JSON
  - every SKILL.md has a 'description' in its YAML frontmatter (the routing trigger)

Exit code 0 on success, 1 on any problem. Run from the repo root:
    python scripts/validate_marketplace.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _frontmatter_has_description(path: str) -> bool:
    """Return True if a Markdown file starts with YAML frontmatter containing description:."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.lstrip().startswith("---"):
        return False
    body = text.lstrip()[3:]
    end = body.find("\n---")
    if end == -1:
        return False
    front = body[:end]
    return any(line.strip().startswith("description:") for line in front.splitlines())


def main() -> int:
    problems: list[str] = []
    mp_path = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")

    try:
        with open(mp_path, encoding="utf-8") as fh:
            mp = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FATAL: cannot read marketplace.json: {exc}")
        return 1

    for field in ("name", "owner", "plugins"):
        if field not in mp:
            problems.append(f"marketplace.json missing required field: {field}")

    plugin_root = mp.get("metadata", {}).get("pluginRoot", "./plugins").lstrip("./")
    seen: set[str] = set()

    for entry in mp.get("plugins", []):
        name = entry.get("name")
        source = entry.get("source")
        if not name or not source:
            problems.append(f"plugin entry missing name/source: {entry!r}")
            continue
        if name in seen:
            problems.append(f"duplicate plugin name: {name}")
        seen.add(name)
        if not isinstance(source, str):
            # Non-local sources (github/url/npm) are not checked on disk.
            continue
        manifest = os.path.join(REPO_ROOT, plugin_root, source, ".claude-plugin", "plugin.json")
        if not os.path.isfile(manifest):
            problems.append(f"{name}: missing manifest at {manifest}")
            continue
        try:
            with open(manifest, encoding="utf-8") as fh:
                m = json.load(fh)
        except json.JSONDecodeError as exc:
            problems.append(f"{name}: invalid plugin.json ({exc})")
            continue
        if m.get("name") != name:
            problems.append(f"{name}: plugin.json name is {m.get('name')!r}")
        if not m.get("description"):
            problems.append(f"{name}: plugin.json missing description")

    for hooks in glob.glob(os.path.join(REPO_ROOT, plugin_root, "*", "hooks", "hooks.json")):
        try:
            with open(hooks, encoding="utf-8") as fh:
                json.load(fh)
        except json.JSONDecodeError as exc:
            problems.append(f"invalid hooks.json: {hooks} ({exc})")

    for skill in glob.glob(os.path.join(REPO_ROOT, plugin_root, "*", "skills", "*", "SKILL.md")):
        if not _frontmatter_has_description(skill):
            problems.append(f"SKILL.md missing 'description' frontmatter: {skill}")

    n_plugins = len(seen)
    if problems:
        print(f"VALIDATION FAILED ({len(problems)} problem(s)) across {n_plugins} plugins:")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"OK: marketplace '{mp.get('name')}' valid — {n_plugins} plugins, all manifests/hooks/skills check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
