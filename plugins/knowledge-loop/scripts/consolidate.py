#!/usr/bin/env python3
"""Consolidation / forgetting pass over the knowledge store (stdlib only).

Memory systems that only ever grow get noisy. This pass does two things, both
grounded in agent-memory literature (Mem0/A-Mem consolidation; exponential
forgetting curves):

1. **Merge near-duplicates** across the whole store — any pair of notes with
   TF-IDF cosine >= DEDUP_THRESHOLD is merged (longer text kept, importance
   bumped, tags unioned, semantic kind wins).
2. **Prune stale, low-value notes** — a note is forgotten when either:
   * it is older than `--max-age-days` (default 365) AND has `importance < 1.0`
     AND was never used (`access_count == 0`); or
   * it is low-confidence (`confidence < 0.3`) AND never used (`access_count == 0`)
     AND older than a short window `--low-conf-age-days` (default 30). An unproven
     lesson that nothing ever corroborated or reused is quietly forgotten.
   Default-importance notes are never pruned by the first rule; default-confidence
   (0.5) notes are never pruned by the second.

Reports how many notes were merged and pruned, then rewrites the store atomically.
Notes with all newer fields absent are defaulted, so an old store consolidates
cleanly. Malformed/blank lines are dropped by this maintenance pass.

Usage:
    consolidate.py [--max-age-days 365] [--low-conf-age-days 30] [--dry-run]
"""

# Confidence at/below which a never-used, stale note is treated as low-value.
LOW_CONFIDENCE_CUTOFF = 0.3

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as kc  # noqa: E402


def merge_duplicates(notes):
    """Greedily merge notes whose pairwise cosine >= DEDUP_THRESHOLD.

    Returns (kept_notes, merged_count).
    """
    if len(notes) < 2:
        return list(notes), 0

    docs_tokens = [kc.tokenize(kc.note_search_text(n)) for n in notes]
    vectors, _idf = kc.build_tfidf(docs_tokens)

    consumed = [False] * len(notes)
    kept = []
    merged_count = 0
    for i in range(len(notes)):
        if consumed[i]:
            continue
        base = notes[i]
        for j in range(i + 1, len(notes)):
            if consumed[j]:
                continue
            if kc.cosine(vectors[i], vectors[j]) >= kc.DEDUP_THRESHOLD:
                base = kc.merge_notes(base, notes[j])
                consumed[j] = True
                merged_count += 1
        kept.append(base)
    return kept, merged_count


def prune_stale(notes, max_age_days, low_conf_age_days, now):
    """Drop stale, low-value notes. Returns (kept, pruned_count).

    Two independent forgetting rules (a note is dropped if it matches either):
      1. stale + low-importance + never-used;
      2. stale (short window) + low-confidence + never-used.
    """
    kept = []
    pruned = 0
    for note in notes:
        age = kc.note_age_days(note, now)
        importance = kc.get_float(note, "importance", kc.DEFAULT_IMPORTANCE)
        confidence = kc.note_confidence(note)
        access = kc.get_int(note, "access_count", 0)

        low_importance_stale = (
            age is not None
            and age > max_age_days
            and importance < kc.DEFAULT_IMPORTANCE
            and access == 0
        )
        low_confidence_stale = (
            age is not None
            and age > low_conf_age_days
            and confidence < LOW_CONFIDENCE_CUTOFF
            and access == 0
        )
        if low_importance_stale or low_confidence_stale:
            pruned += 1
            continue
        kept.append(note)
    return kept, pruned


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Merge near-duplicate learnings and prune stale, low-value ones."
    )
    parser.add_argument(
        "--max-age-days",
        type=float,
        default=365.0,
        help="Prune notes older than this (default 365) when unimportant and unused.",
    )
    parser.add_argument(
        "--low-conf-age-days",
        type=float,
        default=30.0,
        help="Prune notes older than this (default 30) when low-confidence "
             "(< {}) and never used.".format(LOW_CONFIDENCE_CUTOFF),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without rewriting the store.",
    )
    args = parser.parse_args(argv)

    root = kc.project_dir()
    path = kc.store_path(root)
    notes = kc.load_notes(path)
    if not notes:
        print("consolidate: store is empty or missing — nothing to do.")
        return 0

    before = len(notes)
    now = datetime.now(timezone.utc)

    merged_notes, merged_count = merge_duplicates(notes)
    kept, pruned_count = prune_stale(
        merged_notes, args.max_age_days, args.low_conf_age_days, now
    )

    after = len(kept)
    merge_verb = "would merge" if args.dry_run else "merged"
    prune_verb = "would prune" if args.dry_run else "pruned"
    print(
        "consolidate: {} note(s) in, {} out; {} {} duplicate(s), "
        "{} {} stale note(s).".format(
            before, after, merge_verb, merged_count, prune_verb, pruned_count
        )
    )

    if args.dry_run:
        return 0

    if merged_count == 0 and pruned_count == 0:
        return 0

    try:
        kc.write_notes_atomic(path, kept)
    except (OSError, IOError) as exc:
        sys.stderr.write("consolidate.py: could not write store: {}\n".format(exc))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
