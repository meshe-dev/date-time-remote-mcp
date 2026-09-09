"""The generated indexes must match the log and the explorations.

    python3 -m unittest tools/test_build_index.py
"""
import importlib.util
import os
import unittest

_spec = importlib.util.spec_from_file_location("build_index", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_index.py"))
build_index = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_index)


class IndexTests(unittest.TestCase):
    def test_indexes_are_current(self):
        self.assertEqual(build_index.main(["--check"]), 0, "run python3 tools/build_index.py and commit the result")

    def test_every_log_entry_is_indexed_once(self):
        with open(build_index.LOG, encoding="utf-8") as f:
            rows = build_index.parse_log(f.read())
        ids = [r[0] for r in rows]
        self.assertEqual(len(ids), len(set(ids)), "duplicate id in the decision log")
        with open(build_index.DEC_INDEX, encoding="utf-8") as f:
            index = f.read()
        for id_ in ids:
            self.assertIn("| %s |" % id_, index)

    def test_every_exploration_is_indexed(self):
        rows = build_index.explorations()
        with open(build_index.EXP_INDEX, encoding="utf-8") as f:
            index = f.read()
        for r in rows:
            self.assertIn(r[5], index)
        for root, _d, files in os.walk(build_index.DOCS):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                with open(os.path.join(root, fn), encoding="utf-8") as fh:
                    fm = build_index.frontmatter(fh.read())
                if fm.get("type") == "exploration":
                    for k in ("title", "status", "created", "updated", "tags", "related", "description"):
                        self.assertIn(k, fm, "%s missing %s" % (fn, k))

    def test_parent_block_is_embedded_and_current(self):
        # markers present → the block equals the parent's generic rules (when the parent is readable here)
        t = build_index.agreement_target(build_index.AGREEMENT)
        if t is None:
            self.skipTest("no markers or parent not readable on this machine")
        self.assertEqual(t[0], t[1], "run python3 tools/build_index.py — embedded working agreement is stale")

    def test_stamps_with_and_without_time_parse(self):
        rows = build_index.parse_log(
            "**D-001** (2026-09-06, meshe) — **Old style.** body\n"
            "**D-002** (2026-09-08 16:40 PDT, joint) — **New style.** body\n"
            "| O-001 | **Thing.** more | meshe | 2026-09-08 16:41 PDT |\n")
        self.assertEqual([r[0] for r in rows], ["D-001", "D-002", "O-001"])
        self.assertEqual(rows[1][1], "2026-09-08 16:40 PDT")
        self.assertEqual(rows[2][1], "2026-09-08 16:41 PDT")

    def test_embed_replaces_only_between_markers(self):
        parent = "# Parent\n\n*intro*\n\n---\n\n## 1. A\n\nbody a\n\n## 2. B\n\nbody b\n\n---\n\n## Project-specific rules\n\n(none)\n"
        body = build_index.parent_body(parent)
        self.assertTrue(body.startswith("## 1. A") and body.rstrip().endswith("body b"))
        self.assertNotIn("Project-specific", body)
        consumer = "# Mine\n\nhead\n\n<!-- parent:start -->\nold\n<!-- parent:end -->\n\n## Project-specific rules\n\n## 9. Ours\n"
        out = build_index.embed_agreement(consumer, body)
        self.assertIn("## 1. A", out); self.assertNotIn("\nold\n", out); self.assertIn("## 9. Ours", out)
        self.assertRegex(out, r"<!-- parent:start [0-9a-f]{8} -->")
        self.assertEqual(build_index.embed_agreement(out, body), out)  # idempotent
        self.assertEqual(build_index.embed_agreement("no markers here\n", body), "no markers here\n")


if __name__ == "__main__":
    unittest.main()
