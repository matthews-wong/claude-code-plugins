#!/usr/bin/env python3
"""Folder-scoped hybrid retrieval of prior learnings (stdlib only, hook-safe).

Ranking blends several signals grounded in agent-memory literature:

* **Hybrid retrieval + Reciprocal Rank Fusion (RRF).** Candidates are scored by
  BOTH a TF-IDF cosine ranking and a keyword-overlap ranking, then fused with
  `rrf = 1/(K+rank_cosine) + 1/(K+rank_keyword)` (K=60). This is the standard
  "run a vector search and a keyword search in parallel, fuse the two ranked
  lists" recipe (RRF, Cormack et al.).
* **Recency decay.** The fused score is multiplied by `exp(-age_days/HALF_LIFE)`
  so stale lessons fade unless refreshed — a plain exponential forgetting curve.
* **Importance & usefulness.** An optional `importance` field and a usefulness
  boost from `access_count` (`1 + 0.1*log1p(access_count)`) let notes that
  proved valuable rise (Mem0-style importance weighting; Reflexion-style reuse).
* **Confidence.** A gentle multiplier `(0.7 + 0.3*confidence)` so a trustworthy,
  corroborated lesson outranks an equally-relevant unproven one, without letting
  a low-confidence note vanish entirely (confidence-scored memories).
* **Folder-lineage boost.** ×1.5 when a note's folder is an ancestor/descendant.
* **Episodic vs semantic.** Distilled `semantic` principles get a small nudge
  over one-off `episodic` records (A-Mem's semantic/episodic split).

On retrieval it also INCREMENTS `access_count` (and sets `last_used`) for the
notes actually returned, and gives each a small `confidence` bump (a used-and-
survived signal) — best-effort, guarded so a read-only or locked store never
breaks the hook. Always exits 0.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as kc  # noqa: E402

TOP_K = 3
# RRF constant; 60 is the canonical default from the original RRF paper.
RRF_K = 60
# Recency half-life in days for the exp(-age/HALF_LIFE) decay factor.
HALF_LIFE_DAYS = 90.0
# Multiplicative folder-lineage boost (was an additive 0.25; now a factor so it
# composes cleanly with the other multiplicative signals).
FOLDER_BOOST_FACTOR = 1.5
# Small nudge favoring distilled semantic principles over raw episodes.
SEMANTIC_BOOST_FACTOR = 1.1


def rank_map(scored_pairs):
    """Given [(index, score), ...] for hits (score>0), return {index: rank} (0-based)."""
    ordered = sorted(scored_pairs, key=lambda p: p[1], reverse=True)
    return {idx: rank for rank, (idx, _score) in enumerate(ordered)}


def keyword_overlap(query_terms, note_terms):
    """Count of distinct query terms that also appear in the note."""
    if not query_terms or not note_terms:
        return 0
    return len(query_terms & note_terms)


def bump_access(path, ids, when):
    """Best-effort: reinforce the given note ids after they were surfaced.

    Increments access_count, sets last_used, and gives confidence a small bump
    toward 1.0 (used-and-survived signal). Rewrites the store atomically,
    preserving every original line verbatim except the matched notes. Swallows
    every error — retrieval must never fail the hook.
    """
    if not ids:
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw_lines = handle.readlines()
    except (OSError, IOError):
        return

    remaining = set(ids)
    out = []
    for line in raw_lines:
        stripped = line.strip()
        if stripped and remaining:
            try:
                obj = json.loads(stripped)
            except (ValueError, TypeError):
                obj = None
            if isinstance(obj, dict) and obj.get("id") in remaining:
                obj["access_count"] = kc.get_int(obj, "access_count", 0) + 1
                obj["last_used"] = when
                obj["confidence"] = kc.raise_confidence(
                    kc.note_confidence(obj), kc.CONFIDENCE_ACCESS_GAIN
                )
                remaining.discard(obj.get("id"))
                out.append(json.dumps(obj, ensure_ascii=False) + "\n")
                continue
        out.append(line if line.endswith("\n") else line + "\n")

    try:
        tmp = path + ".tmp.{}".format(os.getpid())
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.writelines(out)
        os.replace(tmp, path)
    except (OSError, IOError):
        return


def main():
    root = kc.project_dir()
    path = kc.store_path(root)
    notes = kc.load_notes(path)
    if not notes:
        return 0

    current_folder = kc.rel_folder(root, sys.argv[1] if len(sys.argv) > 1 else "")
    extra_query = " ".join(sys.argv[2:]).strip()

    # The query is the current folder path (segments as words) plus any extra terms.
    query_text = current_folder.replace("/", " ")
    if extra_query:
        query_text = query_text + " " + extra_query

    docs_tokens = [kc.tokenize(kc.note_search_text(note)) for note in notes]
    query_tokens = kc.tokenize(query_text)
    query_term_set = set(query_tokens)

    vectors, idf = kc.build_tfidf(docs_tokens)
    query_vec = kc.vectorize_query(query_tokens, idf)

    # Two parallel ranked lists: cosine hits and keyword-overlap hits.
    cosine_hits = []
    keyword_hits = []
    for i, (note, vec) in enumerate(zip(notes, vectors)):
        cos = kc.cosine(query_vec, vec)
        if cos > 0.0:
            cosine_hits.append((i, cos))
        overlap = keyword_overlap(query_term_set, set(docs_tokens[i]))
        if overlap > 0:
            keyword_hits.append((i, overlap))

    cosine_ranks = rank_map(cosine_hits)
    keyword_ranks = rank_map(keyword_hits)

    # Union of candidates that appeared in at least one list.
    candidate_indices = set(cosine_ranks) | set(keyword_ranks)
    if not candidate_indices:
        return 0

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)

    scored = []
    for i in candidate_indices:
        note = notes[i]

        rrf = 0.0
        if i in cosine_ranks:
            rrf += 1.0 / (RRF_K + cosine_ranks[i])
        if i in keyword_ranks:
            rrf += 1.0 / (RRF_K + keyword_ranks[i])

        # Recency decay: neutral (1.0) when the note has no parseable ts.
        age = kc.note_age_days(note, now)
        recency = 1.0 if age is None else math.exp(-age / HALF_LIFE_DAYS)

        importance = kc.get_float(note, "importance", kc.DEFAULT_IMPORTANCE)
        usefulness = 1.0 + 0.1 * math.log1p(kc.get_int(note, "access_count", 0))
        # Gentle confidence multiplier in [0.7, 1.0]: a corroborated lesson wins a
        # tie over an unproven one, but a low-confidence note is never zeroed out.
        confidence = 0.7 + 0.3 * kc.note_confidence(note)

        score = rrf * recency * importance * usefulness * confidence

        note_folder = kc.rel_folder(root, note.get("folder", "."))
        if kc.folder_related(current_folder, note_folder):
            score *= FOLDER_BOOST_FACTOR

        if kc.note_kind(note) == "semantic":
            score *= SEMANTIC_BOOST_FACTOR

        scored.append((score, i, note))

    scored.sort(key=lambda t: t[0], reverse=True)
    top = [t for t in scored if t[0] > 0.0][:TOP_K]
    if not top:
        return 0

    lines = ["Relevant prior learnings:"]
    returned_ids = []
    for _score, _i, note in top:
        if note.get("id"):
            returned_ids.append(note["id"])
        text = " ".join(str(note.get("text", "")).split())
        if len(text) > 240:
            text = text[:237] + "..."
        folder = note.get("folder", ".")
        kind = kc.note_kind(note)
        tags = kc.note_tags(note)
        tag_str = " [" + ", ".join(tags) + "]" if tags else ""
        lines.append("- ({}, {}){} {}".format(folder, kind, tag_str, text))
    print("\n".join(lines))

    # Reinforce what we surfaced — best-effort, never fatal.
    bump_access(path, returned_ids, kc.now_iso())
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # A retrieval hook must never break the session.
        sys.exit(0)
