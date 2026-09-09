#!/usr/bin/env python3
"""Regenerate docs/Decision-Index.md and docs/Exploration-Index.md.

    python3 tools/build_index.py           # write both
    python3 tools/build_index.py --check   # exit 1 if either is stale (run by the tests)

Decision-Index.md: one line per D/F/P entry and one per O-row in docs/decision-log.md,
in file order. Exploration-Index.md: one line per markdown file under docs/ whose
frontmatter says `type: exploration`. Both are views — the log and the explorations are
the sources. Stdlib only; output is deterministic so a repeated run is a no-op.

Also keeps docs/meta/working-agreement.md in step with its parent: the generic rules live
canonically in ~/Code/docs/meta/working-agreement.md and are EMBEDDED between
`<!-- parent:start … -->` / `<!-- parent:end -->` markers in every project's copy, so every
reader (MCP, phone, git, Obsidian) gets a complete file with nothing to resolve. When the
parent is readable on this machine the block is regenerated (`--check`: stale → exit 1);
when it isn't (a client box) the block is left as-is and the check skips.

    python3 tools/build_index.py --agreement PATH   # refresh the block in one file only
                                                    # (any consumer, e.g. a vault's copy)
"""
import argparse
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, "..", "docs"))
LOG = os.path.join(DOCS, "decision-log.md")
DEC_INDEX = os.path.join(DOCS, "Decision-Index.md")
EXP_INDEX = os.path.join(DOCS, "Exploration-Index.md")
AGREEMENT = os.path.join(DOCS, "meta", "working-agreement.md")
PARENT_AGREEMENT = os.environ.get("RECORD_PARENT_AGREEMENT") or os.path.expanduser("~/Code/docs/meta/working-agreement.md")
MARK_START = re.compile(r"^<!-- parent:start(?: [0-9a-f]{8})? -->$", re.M)
MARK_END = "<!-- parent:end -->"

# Stamps are `YYYY-MM-DD` (entries before 2026-09-08) or `YYYY-MM-DD HH:MM TZ` in America/Vancouver.
STAMP = r"\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2} [A-Z]{2,5})?"
ENTRY = re.compile(r"^\*\*([DFP]-\d{3})\*\* \((" + STAMP + r"), ([^)]+)\) — \*\*(.+?)\*\*")
OROW = re.compile(r"^\| (O-\d{3}) \| (.+?) \| (.+?) \| (.+?) \|$")
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_log(text):
    rows = []
    for line in text.splitlines():
        m = ENTRY.match(line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3), m.group(4).rstrip(".")))
            continue
        m = OROW.match(line)
        if m:
            item = m.group(2)
            bold = re.match(r"\*\*(.+?)\*\*", item)
            head = bold.group(1) if bold else re.split(r"\. ", item, maxsplit=1)[0]
            head = head.rstrip(".?")
            rows.append((m.group(1), m.group(4), "gate: " + m.group(3), head))
    return rows


def render_decision_index(rows):
    out = ["---", "generated: true", "source: decision-log.md", "---", "# Decision Index", "",
           "> Generated from `decision-log.md` by `tools/build_index.py` — do not edit here, edits are overwritten. Navigation, never canon.", "",
           "| ID | Date / opened | Who / gate | Headline |", "|---|---|---|---|"]
    for id_, date, who, head in rows:
        out.append("| %s | %s | %s | %s |" % (id_, date, who, head.replace("|", "\\|")))
    return "\n".join(out) + "\n"


def frontmatter(text):
    m = FRONT.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def explorations():
    rows = []
    for root, _dirs, files in os.walk(DOCS):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, encoding="utf-8") as fh:
                fm = frontmatter(fh.read())
            if fm.get("type") != "exploration":
                continue
            rel = os.path.relpath(path, DOCS).replace(os.sep, "/")
            rows.append((fm.get("title", f), fm.get("status", ""), fm.get("updated", ""),
                         fm.get("tags", "").strip("[]"), fm.get("description", ""), rel,
                         fm.get("related", "").strip("[]")))
    return sorted(rows, key=lambda r: r[5])


def render_exploration_index(rows):
    out = ["---", "generated: true", "source: explorations/", "---", "# Exploration Index", "",
           "> Generated from every `docs/**/*.md` with `type: exploration` by `tools/build_index.py` — do not edit here, edits are overwritten.", "",
           "| Title | Status | Updated | Tags | Description | Source | Related |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return "\n".join(out) + "\n"


def parent_body(text):
    """The generic rules of the parent: from its first `## ` heading up to the
    `## Project-specific rules` heading (and the rule before it), exclusive."""
    m = re.search(r"^## ", text, re.M)
    if not m:
        return ""
    body = text[m.start():]
    cut = re.search(r"^(?:---\s*\n\s*)?## Project-specific rules", body, re.M)
    if cut:
        body = body[:cut.start()]
    return body.rstrip() + "\n"


def embed_agreement(text, body):
    """Replace the block between the markers with `body`; unchanged text if no markers."""
    m = MARK_START.search(text)
    end = text.find(MARK_END)
    if not m or end < 0 or end < m.start():
        return text
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]
    return text[:m.start()] + "<!-- parent:start %s -->\n" % digest + body + text[end:]


def agreement_target(path):
    """Return (current, wanted) for one consumer file, or None when nothing applies:
    no such file, no markers, the file IS the parent, or the parent isn't readable here."""
    if not os.path.isfile(path) or not os.path.isfile(PARENT_AGREEMENT):
        return None
    if os.path.realpath(path) == os.path.realpath(PARENT_AGREEMENT):
        return None
    with open(path, encoding="utf-8") as f:
        have = f.read()
    if not MARK_START.search(have):
        return None
    with open(PARENT_AGREEMENT, encoding="utf-8") as f:
        body = parent_body(f.read())
    return have, embed_agreement(have, body)


def build():
    with open(LOG, encoding="utf-8") as f:
        log = f.read()
    out = {DEC_INDEX: render_decision_index(parse_log(log)), EXP_INDEX: render_exploration_index(explorations())}
    t = agreement_target(AGREEMENT)
    if t:
        out[AGREEMENT] = t[1]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if an index is stale; write nothing")
    ap.add_argument("--agreement", metavar="PATH", help="refresh the embedded parent block in this one file and exit")
    args = ap.parse_args(argv)
    if args.agreement:
        t = agreement_target(os.path.abspath(args.agreement))
        if not t:
            print("nothing to do: no markers, file is the parent, or parent unreadable (%s)" % PARENT_AGREEMENT, file=sys.stderr)
            return 2
        if t[0] == t[1]:
            print("agreement current")
            return 0
        if args.check:
            print("stale: " + args.agreement, file=sys.stderr)
            return 1
        with open(args.agreement, "w", encoding="utf-8") as f:
            f.write(t[1])
        print("refreshed: " + args.agreement)
        return 0
    stale = []
    for path, want in build().items():
        have = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                have = f.read()
        if have != want:
            stale.append(os.path.relpath(path, os.path.dirname(HERE)))
            if not args.check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(want)
    if args.check and stale:
        print("stale: " + ", ".join(stale) + " — run python3 tools/build_index.py", file=sys.stderr)
        return 1
    print("regenerated: " + ", ".join(stale) if stale else "indexes current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
