#!/usr/bin/env python3
"""memory.py — one dependency-free CLI for the unified memory + auto-learning system.

This single tool combines two layers of the same memory system into one install:

  * NOTES (episodic + semantic learnings) — captured cheaply as work happens,
    retrieved by a folder-scoped HYBRID search (TF-IDF cosine + keyword overlap,
    fused with reciprocal rank fusion, then reweighted by recency, importance,
    usefulness and confidence). Merged in from the knowledge-loop plugin.
  * INSTINCTS (durable, promoted rules) — recurring lessons graduate into
    high-confidence rules that are auto-surfaced every session. The
    support/confidence model (`confidence = 1 - 0.5 ** support`), Jaccard dedup,
    and cluster-based promotion are merged in from the instincts plugin.

Both stores live under ONE directory: `.claude/memory/`
  * notes.jsonl     — learnings
  * instincts.jsonl — rules

Pure Python 3, standard library only — this runs from Claude Code hooks, so it
must never import a third-party package and must never crash the session. Every
subcommand is robust to a missing store and exits 0 in that case.

Subcommands:
    remember    add a learning note (dedup-on-ingest merges near-duplicates)
    learn       alias of remember
    recall      folder-scoped hybrid retrieval of learnings (bumps access)
    instincts   list active rules for a scope (used by the SessionStart surface)
    promote     graduate recurring / semantic learnings into instincts
    status      dashboard across both stores
    export      export BOTH notes + instincts to one portable JSON file
    import      merge BOTH from a portable JSON file (dedup / reinforce)
    consolidate merge duplicate notes + prune stale, low-value ones
"""

import argparse
import json
import math
import os
import re
import sys
import time
import uuid
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as mem  # noqa: E402


# ===========================================================================
# NOTES: retrieval knobs (merged from knowledge-loop/retrieve.py)
# ===========================================================================

TOP_K = 3
# RRF constant; 60 is the canonical default from the original RRF paper.
RRF_K = 60
# Recency half-life in days for the exp(-age/HALF_LIFE) decay factor.
HALF_LIFE_DAYS = 90.0
# Multiplicative folder-lineage boost (composes with the other multiplicative signals).
FOLDER_BOOST_FACTOR = 1.5
# Small nudge favoring distilled semantic principles over raw episodes.
SEMANTIC_BOOST_FACTOR = 1.1

# Consolidation: confidence at/below which a never-used, stale note is low-value.
LOW_CONFIDENCE_CUTOFF = 0.3


# ===========================================================================
# INSTINCTS: support/confidence model (merged from instincts/instincts.py)
# ===========================================================================

_INST_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "is", "are",
    "be", "this", "that", "it", "with", "as", "at", "by", "always", "should",
    "must", "when", "before", "after", "prior", "then", "do", "please",
}

_INST_WORD = re.compile(r"[a-z0-9]+")

# Jaccard overlap at/above which two rules in the same scope are the "same" rule.
INSTINCT_SIMILARITY_THRESHOLD = 0.8


def now_utc_iso():
    """UTC 'Z' timestamp — the schema instinct records have always used."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def inst_tokens(text):
    """Normalise rule text into a set of meaningful lowercase tokens."""
    words = _INST_WORD.findall((text or "").lower())
    return {w for w in words if w not in _INST_STOPWORDS and len(w) > 1}


def inst_similarity(a, b):
    """Jaccard token overlap in [0, 1]. 1.0 == identical token sets."""
    ta, tb = inst_tokens(a), inst_tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0


def confidence_for(support):
    """Map a support count to a confidence in (0, 1): confidence = 1 - 0.5 ** support."""
    support = max(1, int(support))
    return round(1 - 0.5 ** support, 4)


def load_instincts(path):
    """Read all instinct records. Tolerant of a missing file or bad lines."""
    records = []
    if not os.path.exists(path):
        return records
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except (ValueError, TypeError):
                    continue
    except OSError:
        return records
    return records


def save_instincts(records, path):
    """Persist all instinct records atomically, creating the store dir if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp.{}".format(os.getpid())
    with open(tmp, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    os.replace(tmp, path)


def inst_scope_for_folder(folder):
    """A repo-root learning (folder '.') promotes to the 'global' scope; else the folder.

    This is an integration improvement over the two separate plugins: instinct
    scopes reuse the note folder vocabulary, so folder-lineage matching (below)
    lines up between the two stores.
    """
    return "global" if folder in (".", "", None) else folder


def find_similar_instinct(records, rule, scope):
    """Return the first same-scope record whose rule is >= threshold similar."""
    for rec in records:
        if rec.get("scope") != scope:
            continue
        if inst_similarity(rec.get("rule", ""), rule) >= INSTINCT_SIMILARITY_THRESHOLD:
            return rec
    return None


def reinforce_instinct(rec, extra_tags=None):
    """Bump support/confidence and merge tags on an existing instinct."""
    rec["support"] = int(rec.get("support", 1)) + 1
    rec["confidence"] = confidence_for(rec["support"])
    rec["updated"] = now_utc_iso()
    if extra_tags:
        merged = list(dict.fromkeys(list(rec.get("tags", [])) + list(extra_tags)))
        rec["tags"] = merged
    return rec


def new_instinct(rule, scope, tags):
    stamp = now_utc_iso()
    return {
        "id": uuid.uuid4().hex[:12],
        "rule": rule.strip(),
        "scope": scope,
        "tags": list(tags or []),
        "confidence": confidence_for(1),
        "support": 1,
        "created": stamp,
        "updated": stamp,
    }


def upsert_instinct(records, rule, scope, tags):
    """Add a new instinct, or reinforce a near-duplicate in the same scope.

    Returns (record, action) where action is 'added' or 'reinforced'.
    """
    rule = (rule or "").strip()
    if not rule:
        raise ValueError("rule text is required and cannot be empty")
    existing = find_similar_instinct(records, rule, scope)
    if existing is not None:
        reinforce_instinct(existing, tags)
        return existing, "reinforced"
    rec = new_instinct(rule, scope, tags)
    records.append(rec)
    return rec, "added"


def sort_instincts_for_scope(records, scope=None):
    """Sort by scope relevance (matching/lineage first, then global), then confidence."""
    def key(rec):
        rec_scope = rec.get("scope", "global")
        if scope is not None and scope != "global" and rec_scope != "global" \
                and mem.folder_related(scope, rec_scope):
            rank = 0
        elif rec_scope == "global":
            rank = 1
        else:
            rank = 2
        return (rank, -float(rec.get("confidence", 0)), -int(rec.get("support", 0)))
    return sorted(records, key=key)


def format_instinct_line(rec):
    tags = ",".join(rec.get("tags", []))
    tag_str = " [%s]" % tags if tags else ""
    return "- (%s | conf %.2f | x%d) %s%s" % (
        rec.get("scope", "global"),
        float(rec.get("confidence", 0)),
        int(rec.get("support", 1)),
        rec.get("rule", ""),
        tag_str,
    )


# ===========================================================================
# NOTES: ingest / dedup helpers (merged from knowledge-loop/store.py)
# ===========================================================================

def parse_tags(raw):
    """Accept comma- or whitespace-separated tags."""
    if not raw:
        return []
    parts = [t.strip() for chunk in raw.split(",") for t in chunk.split()]
    return [t for t in parts if t]


def find_duplicate(incoming, existing_same_folder):
    """Return (original_index, similarity) of the closest same-folder note.

    `existing_same_folder` is a list of (original_index, note) pairs. Both sides
    are represented by `note_search_text` so the comparison is symmetric.
    """
    if not existing_same_folder:
        return None, 0.0
    docs_tokens = [mem.tokenize(mem.note_search_text(note)) for _idx, note in existing_same_folder]
    docs_tokens.append(mem.tokenize(mem.note_search_text(incoming)))
    vectors, _idf = mem.build_tfidf(docs_tokens)
    new_vec = vectors[-1]

    best_pos, best_sim = None, 0.0
    for pos, vec in enumerate(vectors[:-1]):
        sim = mem.cosine(new_vec, vec)
        if sim > best_sim:
            best_pos, best_sim = pos, sim
    if best_pos is None:
        return None, 0.0
    return existing_same_folder[best_pos][0], best_sim


def add_note_to_list(existing, incoming, root):
    """Dedup-on-ingest into an in-memory list. Returns (action, note).

    action is 'merged' (folded into a near-duplicate in the same folder) or
    'stored' (appended as new). Mutates `existing` in place.
    """
    folder = incoming.get("folder", ".")
    same_folder = [
        (i, note) for i, note in enumerate(existing)
        if mem.rel_folder(root, note.get("folder", ".")) == folder
    ]
    dup_index, sim = find_duplicate(incoming, same_folder)
    if dup_index is not None and sim >= mem.DEDUP_THRESHOLD:
        merged = mem.merge_notes(existing[dup_index], incoming)
        existing[dup_index] = merged
        return "merged", merged
    existing.append(incoming)
    return "stored", incoming


# ===========================================================================
# Subcommand: remember / learn
# ===========================================================================

def cmd_remember(args):
    text = (args.text or "").strip()
    if not text:
        sys.stderr.write("memory: --text must not be empty\n")
        return 1

    root = mem.project_dir()
    folder = mem.rel_folder(root, args.folder)
    tags = parse_tags(args.tags)
    store_file = mem.store_path(root)

    incoming = mem.new_note(
        text, folder, tags,
        kind=args.kind, importance=args.importance, confidence=args.confidence,
    )

    existing = mem.load_notes(store_file)
    same_folder = [
        (i, note) for i, note in enumerate(existing)
        if mem.rel_folder(root, note.get("folder", ".")) == folder
    ]
    dup_index, sim = find_duplicate(incoming, same_folder)

    try:
        if dup_index is not None and sim >= mem.DEDUP_THRESHOLD:
            merged = mem.merge_notes(existing[dup_index], incoming)
            existing[dup_index] = merged
            mem.write_notes_atomic(store_file, existing)
            print(
                "Merged into existing learning {} (folder: {}, similarity {:.2f}); "
                "importance now {}, confidence now {}".format(
                    merged.get("id"), folder, sim,
                    merged.get("importance"), merged.get("confidence"),
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
        sys.stderr.write("memory: could not write notes store: {}\n".format(exc))
        return 1
    return 0


# ===========================================================================
# Subcommand: recall (hybrid retrieval, bumps access)
# ===========================================================================

def _rank_map(scored_pairs):
    """Given [(index, score), ...] for hits (score>0), return {index: rank} (0-based)."""
    ordered = sorted(scored_pairs, key=lambda p: p[1], reverse=True)
    return {idx: rank for rank, (idx, _score) in enumerate(ordered)}


def _keyword_overlap(query_terms, note_terms):
    """Count of distinct query terms that also appear in the note."""
    if not query_terms or not note_terms:
        return 0
    return len(query_terms & note_terms)


def _bump_access(path, ids, when):
    """Best-effort: reinforce surfaced note ids. Swallows every error."""
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
                obj["access_count"] = mem.get_int(obj, "access_count", 0) + 1
                obj["last_used"] = when
                obj["confidence"] = mem.raise_confidence(
                    mem.note_confidence(obj), mem.CONFIDENCE_ACCESS_GAIN
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


def cmd_recall(args):
    root = mem.project_dir()
    path = mem.store_path(root)
    notes = mem.load_notes(path)
    if not notes:
        return 0

    current_folder = mem.rel_folder(root, args.folder or "")
    extra_query = " ".join(args.query or []).strip()

    query_text = current_folder.replace("/", " ")
    if extra_query:
        query_text = query_text + " " + extra_query

    docs_tokens = [mem.tokenize(mem.note_search_text(note)) for note in notes]
    query_tokens = mem.tokenize(query_text)
    query_term_set = set(query_tokens)

    vectors, idf = mem.build_tfidf(docs_tokens)
    query_vec = mem.vectorize_query(query_tokens, idf)

    # Two parallel ranked lists: cosine hits and keyword-overlap hits.
    cosine_hits = []
    keyword_hits = []
    for i, (note, vec) in enumerate(zip(notes, vectors)):
        cos = mem.cosine(query_vec, vec)
        if cos > 0.0:
            cosine_hits.append((i, cos))
        overlap = _keyword_overlap(query_term_set, set(docs_tokens[i]))
        if overlap > 0:
            keyword_hits.append((i, overlap))

    cosine_ranks = _rank_map(cosine_hits)
    keyword_ranks = _rank_map(keyword_hits)

    candidate_indices = set(cosine_ranks) | set(keyword_ranks)
    if not candidate_indices:
        return 0

    now = datetime.now(timezone.utc)

    scored = []
    for i in candidate_indices:
        note = notes[i]

        rrf = 0.0
        if i in cosine_ranks:
            rrf += 1.0 / (RRF_K + cosine_ranks[i])
        if i in keyword_ranks:
            rrf += 1.0 / (RRF_K + keyword_ranks[i])

        age = mem.note_age_days(note, now)
        recency = 1.0 if age is None else math.exp(-age / HALF_LIFE_DAYS)

        importance = mem.get_float(note, "importance", mem.DEFAULT_IMPORTANCE)
        usefulness = 1.0 + 0.1 * math.log1p(mem.get_int(note, "access_count", 0))
        confidence = 0.7 + 0.3 * mem.note_confidence(note)

        score = rrf * recency * importance * usefulness * confidence

        note_folder = mem.rel_folder(root, note.get("folder", "."))
        if mem.folder_related(current_folder, note_folder):
            score *= FOLDER_BOOST_FACTOR

        if mem.note_kind(note) == "semantic":
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
        kind = mem.note_kind(note)
        tags = mem.note_tags(note)
        tag_str = " [" + ", ".join(tags) + "]" if tags else ""
        lines.append("- ({}, {}){} {}".format(folder, kind, tag_str, text))
    print("\n".join(lines))

    # Reinforce what we surfaced — best-effort, never fatal.
    _bump_access(path, returned_ids, mem.now_iso())
    return 0


# ===========================================================================
# Subcommand: instincts (list active rules for a scope)
# ===========================================================================

def cmd_instincts(args):
    root = mem.project_dir()
    path = mem.instincts_path(root)
    records = load_instincts(path)
    if not records:
        return 0

    # Normalise the requested scope to the note-folder vocabulary. The literal
    # "global" is preserved; anything else is treated as a folder path.
    if args.scope in (None, "", "global"):
        scope = None if args.scope in (None, "") else "global"
    else:
        scope = mem.rel_folder(root, args.scope)

    active = []
    for rec in records:
        rec_scope = rec.get("scope", "global")
        if rec_scope == "global":
            keep = True
        elif scope is None or scope == "global":
            keep = args.all
        else:
            keep = mem.folder_related(scope, rec_scope)
        if not keep:
            continue
        if args.min_confidence is not None and \
                float(rec.get("confidence", 0)) < args.min_confidence:
            continue
        active.append(rec)

    if not active:
        return 0
    for rec in sort_instincts_for_scope(active, scope):
        print(format_instinct_line(rec))
    return 0


# ===========================================================================
# Subcommand: promote (recurring / semantic learnings -> instincts)
# ===========================================================================

def cluster_notes_jaccard(notes, threshold=INSTINCT_SIMILARITY_THRESHOLD):
    """Greedy single-link clustering by Jaccard token overlap of note text."""
    clusters = []
    for note in notes:
        placed = False
        for cluster in clusters:
            if any(inst_similarity(note.get("text", ""), m.get("text", "")) >= threshold
                   for m in cluster):
                cluster.append(note)
                placed = True
                break
        if not placed:
            clusters.append([note])
    return clusters


def summarize_rule(text):
    """Condense a note into a concise one-line rule."""
    text = " ".join((text or "").split())
    if len(text) > 160:
        text = text[:157].rstrip() + "..."
    return text


def cmd_promote(args):
    root = mem.project_dir()
    notes = mem.load_notes(mem.store_path(root))
    if not notes:
        print("promote: no learnings found; nothing to promote.")
        return 0

    inst_file = mem.instincts_path(root)
    records = load_instincts(inst_file)
    min_support = args.min_support
    promoted = 0
    reinforced = 0

    # 1) Semantic notes graduate on their own (they are already distilled).
    semantic = [n for n in notes if mem.note_kind(n) == "semantic"]
    for note in semantic:
        folder = mem.rel_folder(root, note.get("folder", "."))
        scope = inst_scope_for_folder(folder)
        _, action = upsert_instinct(records, summarize_rule(note.get("text")),
                                    scope, mem.note_tags(note))
        if action == "added":
            promoted += 1
        else:
            reinforced += 1

    # 2) Recurring lessons: cluster the remaining notes and promote any cluster
    #    that recurs (>= min_support members).
    rest = [n for n in notes if mem.note_kind(n) != "semantic"]
    for cluster in cluster_notes_jaccard(rest):
        if len(cluster) < min_support:
            continue
        rep = max(cluster, key=lambda n: len(n.get("text", "")))
        folder = mem.rel_folder(root, rep.get("folder", "."))
        scope = inst_scope_for_folder(folder)
        merged_tags = []
        for n in cluster:
            for t in mem.note_tags(n):
                if t not in merged_tags:
                    merged_tags.append(t)
        rec, action = upsert_instinct(records, summarize_rule(rep.get("text")),
                                      scope, merged_tags)
        # A recurring cluster of N notes is stronger evidence than a single add;
        # credit the extra observations as reinforcements.
        for _ in range(len(cluster) - 1):
            reinforce_instinct(rec, merged_tags)
        if action == "added":
            promoted += 1
        else:
            reinforced += 1

    try:
        save_instincts(records, inst_file)
    except (OSError, IOError) as exc:
        sys.stderr.write("memory: could not write instincts store: {}\n".format(exc))
        return 1
    print("Promotion complete: %d promoted, %d reinforced (from %d learnings)."
          % (promoted, reinforced, len(notes)))
    return 0


# ===========================================================================
# Subcommand: status (dashboard across both stores)
# ===========================================================================

def _file_size(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def cmd_status(args):
    root = mem.project_dir()
    notes_file = mem.store_path(root)
    inst_file = mem.instincts_path(root)
    notes = mem.load_notes(notes_file)
    instincts = load_instincts(inst_file)

    print("Memory store: %s" % mem.memory_dir(root))
    print("")

    # --- Notes -------------------------------------------------------------
    n_total = len(notes)
    by_kind = Counter(mem.note_kind(n) for n in notes)
    print("Learnings (notes.jsonl): %d total" % n_total)
    if n_total:
        kind_str = ", ".join("%s: %d" % (k, by_kind.get(k, 0)) for k in mem.VALID_KINDS)
        avg_note_conf = sum(mem.note_confidence(n) for n in notes) / n_total
        print("  by kind: %s" % kind_str)
        print("  avg confidence: %.2f" % avg_note_conf)

    print("")

    # --- Instincts ---------------------------------------------------------
    i_total = len(instincts)
    print("Instincts (instincts.jsonl): %d total" % i_total)
    if i_total:
        by_scope = Counter(r.get("scope", "global") for r in instincts)
        avg_inst_conf = sum(float(r.get("confidence", 0)) for r in instincts) / i_total
        print("  by scope: %s" % ", ".join(
            "%s: %d" % (s, by_scope[s]) for s in sorted(by_scope)))
        print("  avg confidence: %.2f" % avg_inst_conf)
        top = sorted(instincts, key=lambda r: -int(r.get("support", 0)))[:3]
        print("  top reinforced:")
        for rec in top:
            print("    x%d (conf %.2f) %s" % (
                int(rec.get("support", 1)),
                float(rec.get("confidence", 0)),
                rec.get("rule", ""),
            ))

    print("")
    print("Store size: notes.jsonl %d bytes, instincts.jsonl %d bytes"
          % (_file_size(notes_file), _file_size(inst_file)))
    return 0


# ===========================================================================
# Subcommand: export / import (BOTH stores, one portable file)
# ===========================================================================

def cmd_export(args):
    root = mem.project_dir()
    notes = mem.load_notes(mem.store_path(root))
    instincts = load_instincts(mem.instincts_path(root))
    payload = {
        "kind": "memory-export",
        "version": 1,
        "exported": now_utc_iso(),
        "notes": notes,
        "instincts": instincts,
    }
    try:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
    except (OSError, IOError) as exc:
        sys.stderr.write("memory: could not write export: {}\n".format(exc))
        return 1
    print("Exported %d learning(s) and %d instinct(s) to %s"
          % (len(notes), len(instincts), args.out))
    return 0


def cmd_import(args):
    in_path = getattr(args, "in")
    try:
        with open(in_path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, IOError, ValueError) as exc:
        sys.stderr.write("memory: could not read import file: {}\n".format(exc))
        return 1

    if isinstance(payload, dict):
        incoming_notes = payload.get("notes") or []
        incoming_instincts = payload.get("instincts") or []
    elif isinstance(payload, list):
        # A bare list is treated as instinct records (legacy instincts export).
        incoming_notes = []
        incoming_instincts = payload
    else:
        incoming_notes = []
        incoming_instincts = []

    root = mem.project_dir()

    # --- Notes: dedup-on-ingest per folder --------------------------------
    # Preserve the incoming record faithfully (id, ts, access_count, last_used)
    # so export -> import is a true backup, not a re-observation; dedup still
    # merges a note that near-duplicates one already in the same folder.
    notes_file = mem.store_path(root)
    existing_notes = mem.load_notes(notes_file)
    notes_added = notes_merged = 0
    for item in incoming_notes:
        if not isinstance(item, dict) or not item.get("text"):
            continue
        folder = mem.rel_folder(root, item.get("folder", "."))
        incoming = {
            "id": item.get("id") or uuid.uuid4().hex[:12],
            "text": item.get("text"),
            "folder": folder,
            "tags": mem.note_tags(item),
            "kind": mem.note_kind(item),
            "importance": round(mem.get_float(item, "importance", mem.DEFAULT_IMPORTANCE), 3),
            "confidence": round(mem.note_confidence(item), 4),
            "access_count": mem.get_int(item, "access_count", 0),
            "ts": item.get("ts") or mem.now_iso(),
        }
        if item.get("last_used"):
            incoming["last_used"] = item["last_used"]
        action, _note = add_note_to_list(existing_notes, incoming, root)
        if action == "merged":
            notes_merged += 1
        else:
            notes_added += 1
    if incoming_notes:
        try:
            mem.write_notes_atomic(notes_file, existing_notes)
        except (OSError, IOError) as exc:
            sys.stderr.write("memory: could not write notes store: {}\n".format(exc))
            return 1

    # --- Instincts: dedup / reinforce -------------------------------------
    inst_file = mem.instincts_path(root)
    existing_inst = load_instincts(inst_file)
    inst_added = inst_reinforced = 0
    for item in incoming_instincts:
        if not isinstance(item, dict) or not item.get("rule"):
            continue
        scope = item.get("scope", "global")
        rule = (item.get("rule") or "").strip()
        if not rule:
            continue
        existing = find_similar_instinct(existing_inst, rule, scope)
        if existing is not None:
            # Same rule already here: fold the incoming support in as reinforcement.
            existing["support"] = int(existing.get("support", 1)) + max(
                1, int(item.get("support", 1)))
            existing["confidence"] = confidence_for(existing["support"])
            existing["updated"] = now_utc_iso()
            merged = list(dict.fromkeys(
                list(existing.get("tags", [])) + list(item.get("tags") or [])))
            existing["tags"] = merged
            inst_reinforced += 1
        else:
            # New rule: preserve the incoming record faithfully (support,
            # created) so a round-trip does not silently reset a rule's history.
            support = max(1, int(item.get("support", 1)))
            existing_inst.append({
                "id": item.get("id") or uuid.uuid4().hex[:12],
                "rule": rule,
                "scope": scope,
                "tags": list(item.get("tags") or []),
                "confidence": confidence_for(support),
                "support": support,
                "created": item.get("created") or now_utc_iso(),
                "updated": item.get("updated") or now_utc_iso(),
            })
            inst_added += 1
    if incoming_instincts:
        try:
            save_instincts(existing_inst, inst_file)
        except (OSError, IOError) as exc:
            sys.stderr.write("memory: could not write instincts store: {}\n".format(exc))
            return 1

    print("Import complete: learnings %d added / %d merged; "
          "instincts %d added / %d reinforced."
          % (notes_added, notes_merged, inst_added, inst_reinforced))
    return 0


# ===========================================================================
# Subcommand: consolidate (merge duplicate notes + prune stale ones)
# ===========================================================================

def merge_duplicate_notes(notes):
    """Greedily merge notes whose pairwise cosine >= DEDUP_THRESHOLD.

    Returns (kept_notes, merged_count).
    """
    if len(notes) < 2:
        return list(notes), 0
    docs_tokens = [mem.tokenize(mem.note_search_text(n)) for n in notes]
    vectors, _idf = mem.build_tfidf(docs_tokens)

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
            if mem.cosine(vectors[i], vectors[j]) >= mem.DEDUP_THRESHOLD:
                base = mem.merge_notes(base, notes[j])
                consumed[j] = True
                merged_count += 1
        kept.append(base)
    return kept, merged_count


def prune_stale_notes(notes, max_age_days, low_conf_age_days, now):
    """Drop stale, low-value notes. Returns (kept, pruned_count)."""
    kept = []
    pruned = 0
    for note in notes:
        age = mem.note_age_days(note, now)
        importance = mem.get_float(note, "importance", mem.DEFAULT_IMPORTANCE)
        confidence = mem.note_confidence(note)
        access = mem.get_int(note, "access_count", 0)

        low_importance_stale = (
            age is not None
            and age > max_age_days
            and importance < mem.DEFAULT_IMPORTANCE
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


def cmd_consolidate(args):
    root = mem.project_dir()
    path = mem.store_path(root)
    notes = mem.load_notes(path)
    if not notes:
        print("consolidate: learnings store is empty or missing — nothing to do.")
        return 0

    before = len(notes)
    now = datetime.now(timezone.utc)

    merged_notes, merged_count = merge_duplicate_notes(notes)
    kept, pruned_count = prune_stale_notes(
        merged_notes, args.max_age_days, args.low_conf_age_days, now
    )

    after = len(kept)
    merge_verb = "would merge" if args.dry_run else "merged"
    prune_verb = "would prune" if args.dry_run else "pruned"
    print(
        "consolidate: {} learning(s) in, {} out; {} {} duplicate(s), "
        "{} {} stale note(s).".format(
            before, after, merge_verb, merged_count, prune_verb, pruned_count
        )
    )

    if args.dry_run:
        return 0
    if merged_count == 0 and pruned_count == 0:
        return 0

    try:
        mem.write_notes_atomic(path, kept)
    except (OSError, IOError) as exc:
        sys.stderr.write("memory: could not write notes store: {}\n".format(exc))
        return 1
    return 0


# ===========================================================================
# Argument parsing
# ===========================================================================

def build_parser():
    parser = argparse.ArgumentParser(
        prog="memory",
        description="Unified memory + auto-learning: folder-scoped learnings with "
                    "hybrid search, plus recurring lessons promoted into durable rules.",
    )
    sub = parser.add_subparsers(dest="command")

    def add_remember(name, help_text):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--text", required=True, help="The lesson (self-contained).")
        p.add_argument("--folder", default="", help="Project-relative folder scope.")
        p.add_argument("--tags", default="", help="Comma/space-separated tags.")
        p.add_argument("--kind", default=mem.DEFAULT_KIND, choices=list(mem.VALID_KINDS),
                       help="episodic = what happened; semantic = a reusable principle.")
        p.add_argument("--importance", type=float, default=mem.DEFAULT_IMPORTANCE,
                       help="Relative importance weight (default 1.0).")
        p.add_argument("--confidence", type=float, default=mem.DEFAULT_CONFIDENCE,
                       help="How trustworthy the lesson is, 0.0-1.0 (default 0.5).")
        p.set_defaults(func=cmd_remember)
        return p

    add_remember("remember", "add (or dedup-merge) a learning note")
    add_remember("learn", "alias of remember")

    p_recall = sub.add_parser("recall", help="folder-scoped hybrid retrieval of learnings")
    p_recall.add_argument("folder", nargs="?", default="",
                          help="Current folder (project-relative or absolute).")
    p_recall.add_argument("query", nargs="*", help="Optional extra query terms.")
    p_recall.set_defaults(func=cmd_recall)

    p_inst = sub.add_parser("instincts", help="list active rules for a scope")
    p_inst.add_argument("--scope", default=None,
                        help="'global' or a folder path (absolute or relative).")
    p_inst.add_argument("--min-confidence", type=float, default=None)
    p_inst.add_argument("--all", action="store_true",
                        help="List every instinct regardless of scope.")
    p_inst.set_defaults(func=cmd_instincts)

    p_promote = sub.add_parser("promote", help="graduate recurring/semantic learnings into instincts")
    p_promote.add_argument("--min-support", type=int, default=2,
                           help="cluster size that counts as recurring (default 2)")
    p_promote.set_defaults(func=cmd_promote)

    p_status = sub.add_parser("status", help="dashboard across both stores")
    p_status.set_defaults(func=cmd_status)

    p_export = sub.add_parser("export", help="export BOTH stores to one portable JSON file")
    p_export.add_argument("--out", required=True)
    p_export.set_defaults(func=cmd_export)

    p_import = sub.add_parser("import", help="merge BOTH stores from a portable JSON file")
    p_import.add_argument("--in", required=True, dest="in")
    p_import.set_defaults(func=cmd_import)

    p_cons = sub.add_parser("consolidate", help="merge duplicate learnings + prune stale ones")
    p_cons.add_argument("--max-age-days", type=float, default=365.0,
                        help="Prune notes older than this (default 365) when unimportant + unused.")
    p_cons.add_argument("--low-conf-age-days", type=float, default=30.0,
                        help="Prune notes older than this (default 30) when low-confidence + unused.")
    p_cons.add_argument("--dry-run", action="store_true",
                        help="Report what would change without rewriting the store.")
    p_cons.set_defaults(func=cmd_consolidate)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except Exception as exc:  # never crash a hook-invoked session
        sys.stderr.write("memory: %s\n" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
