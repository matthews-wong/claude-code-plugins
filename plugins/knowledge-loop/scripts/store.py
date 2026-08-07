#!/usr/bin/env python3
"""Append (or merge) a learning note in the local, folder-scoped knowledge store.

Writes one JSON object per line to .claude/knowledge/notes.jsonl under the project
root (CLAUDE_PROJECT_DIR if set, else cwd). Creates the directory and file if
missing, assigns a unique id and an ISO-8601 timestamp.

Notes carry a `kind` (A-Mem's episodic/semantic split):
  * episodic  = what happened in a session (a specific bug, fix, surprise);
  * semantic  = a distilled, reusable principle or reflection.

Dedup on ingest (Mem0/A-Mem "don't store redundant memories"): before appending,
the new text is compared by TF-IDF cosine to existing notes IN THE SAME FOLDER.
If the closest match is >= DEDUP_THRESHOLD, the note is MERGED into that match
(longer text kept, importance bumped, ts refreshed) instead of adding a duplicate.

Pure Python 3, standard library only.

Usage:
    store.py --text "the lesson" [--folder "relative/path"] [--tags "a,b,c"]
             [--kind episodic|semantic] [--importance 1.0]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as kc  # noqa: E402


def parse_tags(raw):
    if not raw:
        return []
    # Accept comma- or whitespace-separated tags.
    parts = [t.strip() for chunk in raw.split(",") for t in chunk.split()]
    return [t for t in parts if t]


def find_duplicate(incoming, existing_same_folder):
    """Return (index, similarity) of the closest same-folder note, or (None, 0.0).

    Both the incoming and existing notes are represented by `note_search_text` so
    the comparison is symmetric (same fields on both sides).
    `existing_same_folder` is a list of (original_index, note) pairs.
    """
    if not existing_same_folder:
        return None, 0.0
    docs_tokens = [kc.tokenize(kc.note_search_text(note)) for _idx, note in existing_same_folder]
    docs_tokens.append(kc.tokenize(kc.note_search_text(incoming)))
    vectors, _idf = kc.build_tfidf(docs_tokens)
    new_vec = vectors[-1]

    best_pos, best_sim = None, 0.0
    for pos, vec in enumerate(vectors[:-1]):
        sim = kc.cosine(new_vec, vec)
        if sim > best_sim:
            best_pos, best_sim = pos, sim
    if best_pos is None:
        return None, 0.0
    return existing_same_folder[best_pos][0], best_sim


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Append or merge a learning note in the folder-scoped knowledge store."
    )
    parser.add_argument("--text", required=True, help="The lesson (self-contained).")
    parser.add_argument("--folder", default="", help="Project-relative folder scope.")
    parser.add_argument("--tags", default="", help="Comma/space-separated tags.")
    parser.add_argument(
        "--kind",
        default=kc.DEFAULT_KIND,
        choices=list(kc.VALID_KINDS),
        help="episodic = what happened; semantic = a reusable principle/reflection.",
    )
    parser.add_argument(
        "--importance",
        type=float,
        default=kc.DEFAULT_IMPORTANCE,
        help="Relative importance weight (default 1.0).",
    )
    args = parser.parse_args(argv)

    text = args.text.strip()
    if not text:
        sys.stderr.write("store.py: --text must not be empty\n")
        return 1

    root = kc.project_dir()
    folder = kc.rel_folder(root, args.folder)
    tags = parse_tags(args.tags)
    store_file = kc.store_path(root)

    incoming = kc.new_note(text, folder, tags, kind=args.kind, importance=args.importance)

    existing = kc.load_notes(store_file)
    same_folder = [
        (i, note) for i, note in enumerate(existing)
        if kc.rel_folder(root, note.get("folder", ".")) == folder
    ]
    dup_index, sim = find_duplicate(incoming, same_folder)

    try:
        if dup_index is not None and sim >= kc.DEDUP_THRESHOLD:
            # Merge into the near-duplicate rather than adding a second copy.
            merged = kc.merge_notes(existing[dup_index], incoming)
            existing[dup_index] = merged
            kc.write_notes_atomic(store_file, existing)
            print(
                "Merged into existing learning {} (folder: {}, similarity {:.2f}); "
                "importance now {}".format(
                    merged.get("id"), folder, sim, merged.get("importance")
                )
            )
        else:
            os.makedirs(os.path.dirname(store_file), exist_ok=True)
            with open(store_file, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(incoming, ensure_ascii=False) + "\n")
            print(
                "Stored learning {} in {} (folder: {}, kind: {})".format(
                    incoming["id"], store_file, folder, incoming["kind"]
                )
            )
    except (OSError, IOError) as exc:
        sys.stderr.write("store.py: could not write store: {}\n".format(exc))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
