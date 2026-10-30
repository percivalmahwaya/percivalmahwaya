import io, json, sys, unittest
from contextlib import redirect_stderr
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import refresh  # noqa: E402

ACC = {"champion": "two_stage_ml", "scored": [
    {"gameweek": 5, "model": "two_stage_ml", "mae": 1.048, "mae_high_return": 5.116},
    {"gameweek": 5, "model": "form_fdr", "mae": 1.15, "mae_high_return": 4.545},
    {"gameweek": 5, "model": "naive_form", "mae": 1.205, "mae_high_return": 4.5},
    {"gameweek": 6, "model": "two_stage_ml", "mae": 1.001, "mae_high_return": 5.195},
    {"gameweek": 6, "model": "form_fdr", "mae": 1.121, "mae_high_return": 4.792},
    {"gameweek": 6, "model": "naive_form", "mae": 1.228, "mae_high_return": 4.751},
]}
RUNS = {"workflow_runs": [{"conclusion": "success", "updated_at": "2026-10-29T18:31:26Z"}]}


def commit(msg, date, sha="a" * 7):
    return {"commit": {"message": msg, "author": {"date": date}}, "html_url": f"https://github.com/x/y/commit/{sha}"}


COMMITS = {"r1": [commit("add tests", "2026-10-28T10:00:00Z"), commit("data: refresh", "2026-10-29T10:00:00Z")],
           "r2": [commit("fix login [bug] | edge", "2026-10-27T10:00:00Z"), commit("Merge branch x", "2026-10-29T09:00:00Z")],
           "r3": [commit("tune model", "2026-10-26T10:00:00Z")]}
NOW = datetime(2026, 10, 30, 0, 0, tzinfo=timezone.utc)


class Block(unittest.TestCase):
    def test_valid_sources_build_a_block(self):
        b = refresh.build_block(ACC, RUNS, COMMITS, NOW)
        self.assertIn("gameweek 6", b)
        self.assertIn("1.001 against 1.121 and 1.228", b)
        self.assertIn("It loses on high-return players: 5.195 against 4.751 and 4.792", b)
        self.assertIn("Only 2 gameweeks are scored", b)
        self.assertIn("succeeded on 2026-10-29 18:31 UTC", b)

    def test_data_and_merge_commits_are_skipped_and_text_is_escaped(self):
        lines = refresh.commit_lines(COMMITS)
        self.assertEqual(len(lines), 3)
        self.assertTrue(all("data:" not in l and "Merge" not in l for l in lines))
        self.assertIn("fix login bug edge", "\n".join(lines))

    def test_no_em_dash_or_empty_widget_text(self):
        b = refresh.build_block(ACC, RUNS, COMMITS, NOW)
        self.assertNotIn("—", b)
        self.assertNotIn("No activity tracked", b)


class FailsLoudly(unittest.TestCase):
    def test_empty_accuracy_fails(self):
        with self.assertRaises(refresh.SourceError):
            refresh.scoreboard_line({"champion": "two_stage_ml", "scored": []})

    def test_missing_baseline_row_fails(self):
        bad = {"champion": "two_stage_ml", "scored": [r for r in ACC["scored"] if r["model"] != "form_fdr"]}
        with self.assertRaises(refresh.SourceError):
            refresh.scoreboard_line(bad)

    def test_no_pipeline_runs_fails(self):
        with self.assertRaises(refresh.SourceError):
            refresh.pipeline_line({"workflow_runs": []})

    def test_too_few_commits_fails(self):
        with self.assertRaises(refresh.SourceError):
            refresh.commit_lines({"r1": [commit("only one", "2026-10-28T10:00:00Z")]})

    def test_main_returns_1_and_leaves_readme_untouched(self):
        before = refresh.README.read_text(encoding="utf-8")
        with mock.patch.object(refresh, "collect", side_effect=refresh.SourceError("down")), redirect_stderr(io.StringIO()):
            self.assertEqual(refresh.main([]), 1)
        self.assertEqual(refresh.README.read_text(encoding="utf-8"), before)

    def test_unreachable_url_is_a_source_error(self):
        with self.assertRaises(refresh.SourceError):
            refresh.http_json("http://127.0.0.1:9/nothing.json")


class Splice(unittest.TestCase):
    def test_replaces_only_the_marked_region(self):
        t = "top\n<!-- latest:start -->\nold\n<!-- latest:end -->\nbottom\n"
        out = refresh.splice(t, "NEW")
        self.assertEqual(out, "top\n<!-- latest:start -->\nNEW\n<!-- latest:end -->\nbottom\n")

    def test_missing_markers_raise(self):
        with self.assertRaises(ValueError):
            refresh.splice("no markers here", "NEW")


if __name__ == "__main__":
    unittest.main()
