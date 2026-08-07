#!/usr/bin/env python3
"""Folder-scoped retrieval of prior learnings via a hand-rolled TF-IDF + cosine vector search.

Reads the local knowledge store (.claude/knowledge/notes.jsonl), builds a TF-IDF
vector for every note and for the query (current relative folder path plus any extra
args), ranks notes by cosine similarity, and boosts notes whose stored folder is an
ancestor or descendant of the current folder. Prints the top-K matches.

Pure Python 3, standard library only, so it can run from a hook with no pip installs.
Always exits 0 and prints nothing when the store is missing or empty.
"""

import json
import math
import os
import re
import sys
from collections import Counter

TOP_K = 3
# Weight added to a note's cosine score when its folder shares a lineage with the
# current folder (ancestor or descendant). Keeps folder-locality relevant without
# letting it fully override textual relevance.
FOLDER_BOOST = 0.25

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    """Lowercase and split into alphanumeric tokens."""
    return _TOKEN_RE.findall((text or "").lower())


def project_dir():
    """Resolve the project root: CLAUDE_PROJECT_DIR if set, else cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def store_path(root):
    return os.path.join(root, ".claude", "knowledge", "notes.jsonl")


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
    """Normalise a folder argument to a project-relative, POSIX-style path.

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


def main():
    root = project_dir()
    path = store_path(root)
    notes = load_notes(path)
    if not notes:
        return 0

    current_folder = rel_folder(root, sys.argv[1] if len(sys.argv) > 1 else "")
    extra_query = " ".join(sys.argv[2:]).strip()

    # The query is the current folder path (path segments as words) plus any extra
    # terms the caller passed. This is the "search vector" we rank notes against.
    query_text = current_folder.replace("/", " ")
    if extra_query:
        query_text = query_text + " " + extra_query

    docs_tokens = [tokenize(note_search_text(note)) for note in notes]
    query_tokens = tokenize(query_text)

    vectors, idf = build_tfidf(docs_tokens)
    query_vec = vectorize_query(query_tokens, idf)

    scored = []
    for note, vec in zip(notes, vectors):
        score = cosine(query_vec, vec)
        note_folder = rel_folder(root, note.get("folder", "."))
        if folder_related(current_folder, note_folder):
            score += FOLDER_BOOST
        scored.append((score, note))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    top = [pair for pair in scored if pair[0] > 0.0][:TOP_K]
    if not top:
        return 0

    lines = ["Relevant prior learnings:"]
    for score, note in top:
        text = " ".join(str(note.get("text", "")).split())
        if len(text) > 240:
            text = text[:237] + "..."
        folder = note.get("folder", ".")
        tags = note.get("tags")
        tag_str = ""
        if isinstance(tags, list) and tags:
            tag_str = " [" + ", ".join(str(t) for t in tags) + "]"
        elif tags:
            tag_str = " [" + str(tags) + "]"
        lines.append("- ({}){} {}".format(folder, tag_str, text))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # A retrieval hook must never break the session.
        sys.exit(0)
