#!/usr/bin/env python3
"""instincts.py -- a tiny, dependency-free CLI for durable, learned rules.

An *instinct* is a high-confidence rule the agent should follow (e.g.
"In this repo, always run `make test` before committing"). Instincts are the
promoted layer on top of raw learnings: when the same lesson recurs it
graduates into an instinct that is auto-surfaced every session.

Pure Python 3 standard library only -- this runs from Claude Code hooks, so it
must never import a third-party package and must never crash the session.

Store: <project>/.claude/instincts/instincts.jsonl (one JSON object per line).
Project directory resolves from $CLAUDE_PROJECT_DIR, else the current dir.

Confidence model
----------------
Confidence is a monotone function of ``support`` (the number of times a rule
has been reinforced):

    confidence = 1 - 0.5 ** support

So support=1 -> 0.50, support=2 -> 0.75, support=3 -> 0.875, and it climbs
toward (but never reaches) 1.0. Every reinforcement roughly halves the
remaining doubt. This keeps a brand-new rule modest and lets repeatedly
observed rules dominate the sort order.
"""

import argparse
import json
import os
import re
import sys
import time
import uuid


# --- store location ---------------------------------------------------------

def project_dir():
    """Resolve the project root the hook is running against."""
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def store_path():
    return os.path.join(project_dir(), ".claude", "instincts", "instincts.jsonl")


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# --- persistence ------------------------------------------------------------

def load(path=None):
    """Read all instinct records. Tolerant of a missing file or bad lines."""
    path = path or store_path()
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
                    # Skip a corrupt line rather than lose the whole store.
                    continue
    except OSError:
        return records
    return records


def save(records, path=None):
    """Persist all records, creating the store directory if needed."""
    path = path or store_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    os.replace(tmp, path)


# --- similarity -------------------------------------------------------------

_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "is", "are",
    "be", "this", "that", "it", "with", "as", "at", "by", "always", "should",
    "must", "when", "before", "after", "prior", "then", "do", "please",
}

_WORD = re.compile(r"[a-z0-9]+")


def tokens(text):
    """Normalise text into a set of meaningful lowercase tokens."""
    words = _WORD.findall((text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


def similarity(a, b):
    """Jaccard token overlap in [0, 1]. 1.0 == identical token sets."""
    ta, tb = tokens(a), tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0


SIMILARITY_THRESHOLD = 0.8


def confidence_for(support):
    """Map a support count to a confidence in (0, 1). See module docstring."""
    support = max(1, int(support))
    return round(1 - 0.5 ** support, 4)


# --- core mutation ----------------------------------------------------------

def find_similar(records, rule, scope):
    """Return the first same-scope record whose rule is >= threshold similar."""
    for rec in records:
        if rec.get("scope") != scope:
            continue
        if similarity(rec.get("rule", ""), rule) >= SIMILARITY_THRESHOLD:
            return rec
    return None


def reinforce(rec, extra_tags=None):
    """Bump support/confidence and merge tags on an existing instinct."""
    rec["support"] = int(rec.get("support", 1)) + 1
    rec["confidence"] = confidence_for(rec["support"])
    rec["updated"] = now_iso()
    if extra_tags:
        merged = list(dict.fromkeys(list(rec.get("tags", [])) + list(extra_tags)))
        rec["tags"] = merged
    return rec


def new_record(rule, scope, tags):
    stamp = now_iso()
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


def upsert(records, rule, scope, tags):
    """Add a new instinct, or reinforce a near-duplicate in the same scope.

    Returns a tuple (record, action) where action is 'added' or 'reinforced'.
    """
    rule = (rule or "").strip()
    if not rule:
        raise ValueError("rule text is required and cannot be empty")
    existing = find_similar(records, rule, scope)
    if existing is not None:
        reinforce(existing, tags)
        return existing, "reinforced"
    rec = new_record(rule, scope, tags)
    records.append(rec)
    return rec, "added"


# --- formatting -------------------------------------------------------------

def parse_tags(raw):
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def sort_for_scope(records, scope=None):
    """Sort by scope relevance (matching scope first), then confidence desc."""
    def key(rec):
        rec_scope = rec.get("scope", "global")
        if scope is not None and rec_scope == scope:
            rank = 0
        elif rec_scope == "global":
            rank = 1
        else:
            rank = 2
        return (rank, -float(rec.get("confidence", 0)), -int(rec.get("support", 0)))
    return sorted(records, key=key)


def format_line(rec):
    tags = ",".join(rec.get("tags", []))
    tag_str = " [%s]" % tags if tags else ""
    return "- (%s | conf %.2f | x%d) %s%s" % (
        rec.get("scope", "global"),
        float(rec.get("confidence", 0)),
        int(rec.get("support", 1)),
        rec.get("rule", ""),
        tag_str,
    )


# --- subcommands ------------------------------------------------------------

def cmd_add(args):
    records = load()
    scope = args.scope or "global"
    rec, action = upsert(records, args.rule, scope, parse_tags(args.tags))
    save(records)
    if action == "reinforced":
        print("Reinforced existing instinct (support now x%d, confidence %.2f):"
              % (rec["support"], rec["confidence"]))
    else:
        print("Added new instinct (confidence %.2f):" % rec["confidence"])
    print(format_line(rec))
    return 0


def cmd_list(args):
    records = load()
    if args.scope:
        records = [r for r in records
                   if r.get("scope") == args.scope or r.get("scope") == "global"]
    if args.min_confidence is not None:
        records = [r for r in records
                   if float(r.get("confidence", 0)) >= args.min_confidence]
    records = sort_for_scope(records, args.scope)
    if not records:
        print("No instincts recorded yet.")
        return 0
    for rec in records:
        print(format_line(rec))
    return 0


def cmd_status(args):
    records = load()
    total = len(records)
    print("Instincts store: %s" % store_path())
    print("Total instincts: %d" % total)
    if not total:
        return 0
    by_scope = {}
    for rec in records:
        by_scope[rec.get("scope", "global")] = by_scope.get(rec.get("scope", "global"), 0) + 1
    avg_conf = sum(float(r.get("confidence", 0)) for r in records) / total
    print("Average confidence: %.2f" % avg_conf)
    print("By scope:")
    for scope in sorted(by_scope):
        print("  %s: %d" % (scope, by_scope[scope]))
    top = sorted(records, key=lambda r: -int(r.get("support", 0)))[:3]
    print("Top reinforced:")
    for rec in top:
        print("  x%d %s" % (int(rec.get("support", 1)), rec.get("rule", "")))
    return 0


def cmd_export(args):
    records = load()
    payload = {
        "kind": "instincts-export",
        "version": 1,
        "exported": now_iso(),
        "instincts": records,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print("Exported %d instinct(s) to %s" % (len(records), args.out))
    return 0


def cmd_import(args):
    with open(getattr(args, "in"), "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    incoming = payload.get("instincts") if isinstance(payload, dict) else payload
    if not isinstance(incoming, list):
        print("Import file has no 'instincts' list; nothing to do.")
        return 0
    records = load()
    added = reinforced = 0
    for item in incoming:
        if not isinstance(item, dict) or not item.get("rule"):
            continue
        scope = item.get("scope", "global")
        _, action = upsert(records, item.get("rule"), scope, item.get("tags") or [])
        if action == "added":
            added += 1
        else:
            reinforced += 1
    save(records)
    print("Import complete: %d added, %d reinforced." % (added, reinforced))
    return 0


# --- promotion (auto-learning) ----------------------------------------------

def knowledge_path():
    return os.path.join(project_dir(), ".claude", "knowledge", "notes.jsonl")


def load_notes(path):
    notes = []
    if not os.path.exists(path):
        return notes
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if isinstance(obj, dict) and obj.get("text"):
                    notes.append(obj)
    except OSError:
        return notes
    return notes


def cluster_notes(notes, threshold=SIMILARITY_THRESHOLD):
    """Greedy single-link clustering by token overlap of note text."""
    clusters = []
    for note in notes:
        placed = False
        for cluster in clusters:
            if any(similarity(note.get("text", ""), m.get("text", "")) >= threshold
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
    notes_file = args.notes or knowledge_path()
    notes = load_notes(notes_file)
    if not notes:
        # Robust when the sibling knowledge store is absent: do nothing.
        print("No knowledge notes found at %s; nothing to promote." % notes_file)
        return 0

    records = load()
    min_support = args.min_support
    promoted = 0
    reinforced = 0

    # 1) Semantic notes graduate on their own (they are already distilled).
    semantic = [n for n in notes if n.get("kind") == "semantic"]
    for note in semantic:
        scope = note.get("folder") or "global"
        _, action = upsert(records, summarize_rule(note.get("text")),
                           scope, note.get("tags") or [])
        if action == "added":
            promoted += 1
        else:
            reinforced += 1

    # 2) Recurring lessons: cluster the remaining notes and promote any
    #    cluster that recurs (>= min_support members).
    rest = [n for n in notes if n.get("kind") != "semantic"]
    for cluster in cluster_notes(rest):
        if len(cluster) < min_support:
            continue
        # Represent the cluster by its longest (most descriptive) member.
        rep = max(cluster, key=lambda n: len(n.get("text", "")))
        scope = rep.get("folder") or "global"
        merged_tags = []
        for n in cluster:
            for t in (n.get("tags") or []):
                if t not in merged_tags:
                    merged_tags.append(t)
        rec, action = upsert(records, summarize_rule(rep.get("text")),
                             scope, merged_tags)
        # A recurring cluster of N notes is stronger evidence than a single
        # add; credit the extra observations as reinforcements.
        for _ in range(len(cluster) - 1):
            reinforce(rec, merged_tags)
        if action == "added":
            promoted += 1
        else:
            reinforced += 1

    save(records)
    print("Promotion complete: %d promoted, %d reinforced (from %d notes)."
          % (promoted, reinforced, len(notes)))
    return 0


# --- argument parsing -------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="instincts",
        description="Durable, learned rules the agent should follow.",
    )
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="add or reinforce an instinct")
    p_add.add_argument("--rule", required=True)
    p_add.add_argument("--scope", default="global",
                       help="'global' or a folder path")
    p_add.add_argument("--tags", default="", help="comma-separated tags")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list active instincts")
    p_list.add_argument("--scope", default=None)
    p_list.add_argument("--min-confidence", type=float, default=None)
    p_list.set_defaults(func=cmd_list)

    p_status = sub.add_parser("status", help="summary statistics")
    p_status.set_defaults(func=cmd_status)

    p_export = sub.add_parser("export", help="export all instincts to a file")
    p_export.add_argument("--out", required=True)
    p_export.set_defaults(func=cmd_export)

    p_import = sub.add_parser("import", help="merge instincts from a file")
    p_import.add_argument("--in", required=True, dest="in")
    p_import.set_defaults(func=cmd_import)

    p_promote = sub.add_parser(
        "promote", help="graduate recurring learnings into instincts")
    p_promote.add_argument("--notes", default=None,
                           help="path to knowledge notes.jsonl")
    p_promote.add_argument("--min-support", type=int, default=2,
                           help="cluster size that counts as recurring")
    p_promote.set_defaults(func=cmd_promote)

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
        sys.stderr.write("instincts: %s\n" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
