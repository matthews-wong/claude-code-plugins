#!/usr/bin/env python3
"""Shared helpers for the knowledge-loop scripts (store / retrieve / consolidate).

Pure Python 3, standard library only — these scripts run straight from hooks with
no pip installs. Everything here is deliberately dependency-free.

Backward compatibility: older notes in .claude/knowledge/notes.jsonl may predate
the newer fields (`kind`, `importance`, `access_count`, `last_used`). All readers
here default those fields, so an old store keeps working unchanged.
"""

import json
import math
import os
import re
import uuid
from collections import Counter
from datetime import datetime, timezone

# --- shared knobs (kept here so all three scripts agree) --------------------

# Similarity at/above which two notes are treated as near-duplicates (dedup on
# ingest, and consolidation merges). Grounded in the "merge semantically
# redundant memories" idea from Mem0 / A-Mem.
DEDUP_THRESHOLD = 0.85
# How much a merge bumps a note's importance — a lesson learned twice matters more.
IMPORTANCE_BUMP = 0.5
DEFAULT_IMPORTANCE = 1.0
DEFAULT_KIND = "episodic"
VALID_KINDS = ("episodic", "semantic")

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    """Lowercase and split into alphanumeric tokens."""
    return _TOKEN_RE.findall((text or "").lower())


def project_dir():
    """Resolve the project root: CLAUDE_PROJECT_DIR if set, else cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def store_path(root):
    return os.path.join(root, ".claude", "knowledge", "notes.jsonl")


def now_iso():
    """Current local time as an ISO-8601 string with offset, seconds precision."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_notes(path):
    """Read notes.jsonl, skipping blank or malformed lines. Never raises."""
    notes = []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if isinstance(obj, dict) and obj.get("text"):
                    notes.append(obj)
    except (OSError, IOError):
        return []
    return notes


def rel_folder(root, raw):
    """Normalise a folder to a project-relative, POSIX-style path.

    Accepts an absolute path (converted relative to the project root) or an
    already-relative path. Returns "." for the project root itself.
    """
    if not raw:
        return "."
    raw = raw.strip()
    if os.path.isabs(raw):
        try:
            raw = os.path.relpath(raw, root)
        except ValueError:
            # Different drive on Windows, etc. — fall back to the basename.
            raw = os.path.basename(raw.rstrip("/\\"))
    raw = raw.replace("\\", "/").strip("/")
    return raw or "."


def folder_related(current, other):
    """True when `other` is an ancestor or descendant of `current` (or equal)."""
    if not current or not other:
        return False
    if current == other:
        return True
    cur = "" if current == "." else current
    oth = "" if other == "." else other
    if cur == "" or oth == "":
        # Project root is related to everything.
        return True
    return (cur + "/").startswith(oth + "/") or (oth + "/").startswith(cur + "/")


def build_tfidf(docs_tokens):
    """Return (tfidf_vectors, idf) for a list of token lists."""
    n_docs = len(docs_tokens)
    df = Counter()
    for tokens in docs_tokens:
        for term in set(tokens):
            df[term] += 1
    idf = {}
    for term, count in df.items():
        # Smoothed idf; +1 keeps weights positive even for ubiquitous terms.
        idf[term] = math.log((1 + n_docs) / (1 + count)) + 1.0

    vectors = []
    for tokens in docs_tokens:
        counts = Counter(tokens)
        total = len(tokens) or 1
        vec = {}
        for term, count in counts.items():
            vec[term] = (count / total) * idf.get(term, 0.0)
        vectors.append(vec)
    return vectors, idf


def vectorize_query(tokens, idf):
    counts = Counter(tokens)
    total = len(tokens) or 1
    vec = {}
    for term, count in counts.items():
        if term in idf:
            vec[term] = (count / total) * idf[term]
    return vec


def cosine(a, b):
    if not a or not b:
        return 0.0
    # Iterate the smaller vector for the dot product.
    if len(a) > len(b):
        a, b = b, a
    dot = sum(weight * b.get(term, 0.0) for term, weight in a.items())
    if dot == 0.0:
        return 0.0
    norm_a = math.sqrt(sum(w * w for w in a.values()))
    norm_b = math.sqrt(sum(w * w for w in b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def note_search_text(note):
    """Text used to represent a note: its body, plus tags and folder as context."""
    parts = [note.get("text", "")]
    tags = note.get("tags")
    if isinstance(tags, list):
        parts.extend(str(t) for t in tags)
    elif tags:
        parts.append(str(tags))
    folder = note.get("folder")
    if folder:
        parts.append(str(folder).replace("/", " ").replace("\\", " "))
    return " ".join(parts)


# --- field accessors that default the newer fields for old notes ------------

def get_float(note, key, default):
    try:
        return float(note.get(key, default))
    except (TypeError, ValueError):
        return default


def get_int(note, key, default):
    try:
        return int(note.get(key, default))
    except (TypeError, ValueError):
        return default


def note_kind(note):
    kind = note.get("kind")
    return kind if kind in VALID_KINDS else DEFAULT_KIND


def note_tags(note):
    tags = note.get("tags")
    if isinstance(tags, list):
        return [str(t) for t in tags]
    if tags:
        return [str(tags)]
    return []


def note_age_days(note, now=None):
    """Age of a note in days from its `ts`, or None when `ts` is missing/unparseable."""
    ts = note.get("ts")
    if not ts:
        return None
    try:
        parsed = datetime.fromisoformat(str(ts))
    except (ValueError, TypeError):
        return None
    if now is None:
        now = datetime.now(timezone.utc)
    # Make both sides tz-aware for a correct delta.
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    delta = (now - parsed).total_seconds() / 86400.0
    return max(delta, 0.0)


def merge_notes(a, b):
    """Merge two near-duplicate notes into one, per the Mem0/A-Mem consolidation idea.

    - keep the LONGER text (more context wins)
    - union the tags
    - bump importance (a lesson seen twice matters more)
    - kind: `semantic` wins over `episodic` (a distilled principle outranks an episode)
    - sum access counts; keep the most recent `last_used`
    - refresh `ts` to now (this is a fresh merge event)
    - keep the primary (longer) note's id and folder
    """
    ta, tb = a.get("text", ""), b.get("text", "")
    primary, secondary = (a, b) if len(ta) >= len(tb) else (b, a)

    merged = dict(primary)

    tags = []
    for t in note_tags(a) + note_tags(b):
        if t not in tags:
            tags.append(t)
    merged["tags"] = tags

    imp = max(get_float(a, "importance", DEFAULT_IMPORTANCE),
              get_float(b, "importance", DEFAULT_IMPORTANCE)) + IMPORTANCE_BUMP
    merged["importance"] = round(imp, 3)

    kinds = {note_kind(a), note_kind(b)}
    merged["kind"] = "semantic" if "semantic" in kinds else "episodic"

    merged["access_count"] = get_int(a, "access_count", 0) + get_int(b, "access_count", 0)

    last_used = [x.get("last_used") for x in (a, b) if x.get("last_used")]
    if last_used:
        merged["last_used"] = max(last_used)

    merged["ts"] = now_iso()
    return merged


def new_note(text, folder, tags, kind=DEFAULT_KIND, importance=DEFAULT_IMPORTANCE):
    """Build a fresh note dict with all current fields populated."""
    return {
        "id": uuid.uuid4().hex[:12],
        "text": text,
        "folder": folder,
        "tags": tags,
        "kind": kind if kind in VALID_KINDS else DEFAULT_KIND,
        "importance": round(float(importance), 3),
        "access_count": 0,
        "ts": now_iso(),
    }


def write_notes_atomic(path, notes):
    """Rewrite the whole store from `notes`, atomically. Raises on IO failure."""
    store_dir = os.path.dirname(path)
    os.makedirs(store_dir, exist_ok=True)
    tmp = path + ".tmp.{}".format(os.getpid())
    with open(tmp, "w", encoding="utf-8") as handle:
        for note in notes:
            handle.write(json.dumps(note, ensure_ascii=False) + "\n")
    os.replace(tmp, path)
