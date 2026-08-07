#!/usr/bin/env python3
"""Evolve recurring learnings into DRAFT reusable skills (stdlib only).

This is the auto-learning -> skill loop: when several notes keep circling the
same topic, they have graduated from one-off "instincts" into a reusable pattern
worth promoting to a real skill. `evolve.py` finds those clusters and DRAFTS a
well-formed SKILL.md scaffold for each — it never installs a skill itself; a
human (or the model, via `/evolve`) reviews each draft and promotes the good ones.

How it clusters:
  * Build TF-IDF vectors over every note (same vectorizer the rest of the plugin
    uses) and take pairwise cosine similarity.
  * Single-link / greedy clustering (union-find): two notes join the same cluster
    when their cosine is >= --threshold (default 0.35) AND they share context
    (related folder OR at least one common tag). Connected components are the
    clusters, so a chain of related notes gathers into one group.
  * A cluster is written out only when it has >= --min-size notes (default 3) and
    a decent average confidence (>= --min-confidence, default 0.4) — we do not
    crystallize an unproven or trivial pattern into a skill.

For each qualifying cluster it writes:
    .claude/knowledge/evolved/<slug>/SKILL.md
a valid SKILL.md with frontmatter (`name:` + a routing `description:` synthesized
from the cluster's folder and most common tags) and a body listing the clustered
lessons as guidance. It prints a summary of clusters found and drafts written.

Pure Python 3, standard library only.

Usage:
    evolve.py [--threshold 0.35] [--min-size 3] [--min-confidence 0.4]
              [--out-dir <path>] [--dry-run]
"""

import argparse
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as kc  # noqa: E402

DEFAULT_THRESHOLD = 0.35
DEFAULT_MIN_SIZE = 3
DEFAULT_MIN_CONFIDENCE = 0.4

# Generic tokens that make a poor skill name/description if they lead the slug.
_STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "it", "this", "that", "when", "not", "but", "was", "are", "be", "as", "at",
    "by", "if", "so", "we", "you", "use", "using", "used",
}


class _Union:
    """Minimal union-find for single-link clustering."""

    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def shared_context(note_a, note_b, root):
    """True when two notes share a related folder or at least one tag."""
    fa = kc.rel_folder(root, note_a.get("folder", "."))
    fb = kc.rel_folder(root, note_b.get("folder", "."))
    if kc.folder_related(fa, fb):
        return True
    tags_a = {t.lower() for t in kc.note_tags(note_a)}
    tags_b = {t.lower() for t in kc.note_tags(note_b)}
    return bool(tags_a & tags_b)


def cluster_notes(notes, root, threshold):
    """Single-link clustering by TF-IDF cosine + shared context. Returns clusters
    as lists of note indices (only clusters of size >= 2 are returned)."""
    n = len(notes)
    if n < 2:
        return []
    docs_tokens = [kc.tokenize(kc.note_search_text(note)) for note in notes]
    vectors, _idf = kc.build_tfidf(docs_tokens)

    uf = _Union(n)
    for i in range(n):
        for j in range(i + 1, n):
            if kc.cosine(vectors[i], vectors[j]) < threshold:
                continue
            if shared_context(notes[i], notes[j], root):
                uf.union(i, j)

    groups = {}
    for i in range(n):
        groups.setdefault(uf.find(i), []).append(i)
    return [members for members in groups.values() if len(members) >= 2]


def slugify(text, fallback="learnings"):
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    return text or fallback


def dominant_folder(cluster_notes_list, root):
    folders = [kc.rel_folder(root, n.get("folder", ".")) for n in cluster_notes_list]
    counts = Counter(folders)
    # Prefer a non-root folder if one is common; "." only if it truly dominates.
    ranked = counts.most_common()
    for folder, _c in ranked:
        if folder != ".":
            return folder
    return ranked[0][0] if ranked else "."


def top_tags(cluster_notes_list, limit=5):
    counts = Counter()
    for note in cluster_notes_list:
        for tag in kc.note_tags(note):
            counts[tag.lower()] += 1
    return [tag for tag, _c in counts.most_common(limit)]


def keyword_terms(cluster_notes_list, limit=4):
    """Distinctive content words across the cluster, for naming when tags are thin."""
    counts = Counter()
    for note in cluster_notes_list:
        for tok in kc.tokenize(note.get("text", "")):
            if len(tok) > 2 and tok not in _STOPWORDS:
                counts[tok] += 1
    return [term for term, _c in counts.most_common(limit)]


def build_slug(folder, tags, terms, used):
    parts = []
    if folder and folder != ".":
        parts.append(os.path.basename(folder.rstrip("/")))
    parts.extend(tags[:2] if tags else terms[:2])
    # De-duplicate segments (e.g. folder "auth" + tag "auth") preserving order.
    seen = set()
    unique_parts = []
    for p in parts:
        p = slugify(p, "")
        if p and p not in seen:
            seen.add(p)
            unique_parts.append(p)
    base = slugify("-".join(unique_parts)) or "learnings"
    slug = base
    n = 2
    while slug in used:
        slug = "{}-{}".format(base, n)
        n += 1
    used.add(slug)
    return slug


def build_description(folder, tags, terms, size, avg_conf):
    topics = tags if tags else terms
    topic_str = ", ".join(topics[:4]) if topics else "recurring lessons"
    where = "the `{}` area".format(folder) if folder and folder != "." else "this repo"
    return (
        "Guidance distilled from {n} recurring learnings (avg confidence {c:.2f}) "
        "about {topics} in {where}. Use when working in {where} or on {topics} — "
        "apply these hard-won lessons before re-deriving them."
    ).format(n=size, c=avg_conf, topics=topic_str, where=where)


def render_skill(slug, folder, tags, terms, members, notes):
    cluster = [notes[i] for i in members]
    size = len(cluster)
    avg_conf = sum(kc.note_confidence(n) for n in cluster) / size
    description = build_description(folder, tags, terms, size, avg_conf)
    title = slug.replace("-", " ").title()

    lines = []
    lines.append("---")
    lines.append("name: {}".format(slug))
    lines.append("description: {}".format(description))
    lines.append("---")
    lines.append("")
    lines.append("# {}".format(title))
    lines.append("")
    lines.append(
        "> DRAFT skill auto-evolved by knowledge-loop from {n} recurring learnings "
        "(average confidence {c:.2f}). Review the lessons below, sharpen the "
        "`description:` above into a strong trigger, then promote this into a real "
        "plugin/project skill if it earns its place.".format(n=size, c=avg_conf)
    )
    lines.append("")
    if folder and folder != ".":
        lines.append("Primarily about the `{}` area of the repo.".format(folder))
        lines.append("")
    if tags:
        lines.append("Tags across the cluster: {}.".format(", ".join(tags)))
        lines.append("")
    lines.append("## Lessons")
    lines.append("")
    # Most-corroborated lessons first.
    for note in sorted(cluster, key=kc.note_confidence, reverse=True):
        text = " ".join(str(note.get("text", "")).split())
        conf = kc.note_confidence(note)
        note_folder = note.get("folder", ".")
        lines.append("- {} _(folder: `{}`, confidence {:.2f})_".format(text, note_folder, conf))
    lines.append("")
    lines.append("## How to apply")
    lines.append("")
    lines.append(
        "Treat the lessons above as defaults for this area: check them before "
        "acting, prefer the approach they endorse, and avoid the pitfalls they "
        "name. If one no longer holds, record the correction with `/learn` so the "
        "loop keeps this skill honest."
    )
    lines.append("")
    return "\n".join(lines), avg_conf


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Evolve recurring learnings into DRAFT reusable skills."
    )
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="Cosine similarity to join a cluster (default 0.35).")
    parser.add_argument("--min-size", type=int, default=DEFAULT_MIN_SIZE,
                        help="Minimum notes per cluster to draft a skill (default 3).")
    parser.add_argument("--min-confidence", type=float, default=DEFAULT_MIN_CONFIDENCE,
                        help="Minimum average cluster confidence to draft (default 0.4).")
    parser.add_argument("--out-dir", default="",
                        help="Where to write drafts (default .claude/knowledge/evolved).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report clusters without writing any draft files.")
    args = parser.parse_args(argv)

    root = kc.project_dir()
    path = kc.store_path(root)
    notes = kc.load_notes(path)
    if not notes:
        print("evolve: store is empty or missing — nothing to evolve.")
        return 0

    out_dir = args.out_dir or os.path.join(root, ".claude", "knowledge", "evolved")

    clusters = cluster_notes(notes, root, args.threshold)
    qualifying = []
    for members in clusters:
        if len(members) < args.min_size:
            continue
        avg_conf = sum(kc.note_confidence(notes[i]) for i in members) / len(members)
        if avg_conf < args.min_confidence:
            continue
        qualifying.append(members)

    print(
        "evolve: {} note(s) scanned; {} cluster(s) of size >= 2 found; "
        "{} qualify (size >= {}, avg confidence >= {:.2f}).".format(
            len(notes), len(clusters), len(qualifying),
            args.min_size, args.min_confidence,
        )
    )
    if not qualifying:
        print("evolve: no cluster crossed the bar — nothing drafted.")
        return 0

    used_slugs = set()
    written = 0
    for members in sorted(qualifying, key=len, reverse=True):
        cluster = [notes[i] for i in members]
        folder = dominant_folder(cluster, root)
        tags = top_tags(cluster)
        terms = keyword_terms(cluster)
        slug = build_slug(folder, tags, terms, used_slugs)
        content, avg_conf = render_skill(slug, folder, tags, terms, members, notes)
        target = os.path.join(out_dir, slug, "SKILL.md")

        if args.dry_run:
            print("  would draft: {} ({} lessons, avg confidence {:.2f}) -> {}".format(
                slug, len(members), avg_conf, target))
            continue

        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(content)
        except (OSError, IOError) as exc:
            sys.stderr.write("evolve.py: could not write {}: {}\n".format(target, exc))
            continue
        written += 1
        print("  drafted: {} ({} lessons, avg confidence {:.2f}) -> {}".format(
            slug, len(members), avg_conf, target))

    if not args.dry_run:
        print("evolve: wrote {} draft skill(s) under {}. Review and promote the good ones.".format(
            written, out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
