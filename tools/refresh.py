#!/usr/bin/env python3
"""Refresh the Latest section of README.md from live sources.

Standard library plus the gh CLI. Exits non-zero, and writes nothing, when any
source is empty, malformed or unreachable. A green run therefore means every
source returned real data.

  python tools/refresh.py            rewrite README.md in place
  python tools/refresh.py --print    print the block, change nothing

Exit codes: 0 ok, 1 a source failed or returned nothing, 2 markers missing.
"""
import json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
START, END = "<!-- latest:start -->", "<!-- latest:end -->"

OWNER = "percivalmahwaya"
ACCURACY_URL = os.environ.get(
    "ACCURACY_URL",
    "https://raw.githubusercontent.com/percivalmahwaya/fpl-decision-engine/main/site/data/accuracy.json")
BASELINES = ("form_fdr", "naive_form")
COMMIT_REPOS = ["fpl-decision-engine", "bcachesshub", "crime-hotspot-dss",
                "percivalmahwaya.github.io", "team-project-semester4", "jrm-traditions-challenge"]
SKIP_MESSAGE = re.compile(r"^(data:|merge\b|update readme)", re.I)
MIN_COMMITS, SHOW_COMMITS = 3, 5


class SourceError(Exception):
    pass


def http_json(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except Exception as e:  # network, status, parse
        raise SourceError(f"{url}: {e}")


def gh_json(path):
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
    except Exception as e:
        raise SourceError(f"gh api {path}: {e}")
    if out.returncode != 0:
        raise SourceError(f"gh api {path}: {out.stderr.strip()[:200]}")
    try:
        return json.loads(out.stdout)
    except ValueError as e:
        raise SourceError(f"gh api {path}: bad JSON ({e})")


def scoreboard_line(acc):
    champ = acc.get("champion")
    scored = acc.get("scored") or []
    if not champ or not scored:
        raise SourceError("accuracy.json has no champion or no scored rows")
    last = max(r["gameweek"] for r in scored)

    def row(model):
        for r in scored:
            if r["gameweek"] == last and r["model"] == model:
                return r
        raise SourceError(f"accuracy.json has no gameweek {last} row for {model}")

    c = row(champ)
    a, b = (row(m) for m in BASELINES)
    hr_lo = min(a["mae_high_return"], b["mae_high_return"])
    hr_hi = max(a["mae_high_return"], b["mae_high_return"])
    n = len({r["gameweek"] for r in scored})
    verdict = "It loses on high-return players" if c["mae_high_return"] > hr_hi else "It also leads on high-return players"
    return (f"FPL Decision Engine scoreboard, gameweek {last}: model error (MAE) {c['mae']:.3f} "
            f"against {a['mae']:.3f} and {b['mae']:.3f} for the two baselines. Lower is better. "
            f"{verdict}: {c['mae_high_return']:.3f} against {hr_lo:.3f} and {hr_hi:.3f}. "
            f"Only {n} gameweeks are scored.")


def pipeline_line(runs):
    items = (runs or {}).get("workflow_runs") or []
    if not items:
        raise SourceError("no completed pipeline runs returned")
    r = items[0]
    when = r["updated_at"].replace("T", " ")[:16] + " UTC"
    word = {"success": "succeeded", "failure": "failed", "cancelled": "was cancelled"}.get(r["conclusion"], str(r["conclusion"]))
    return f"FPL pipeline: the last completed run {word} on {when}."


def clean(text):
    text = text.splitlines()[0] if text else ""
    text = re.sub(r"[\[\]|`<>]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:77] + "...") if len(text) > 80 else text


def commit_lines(per_repo):
    rows = []
    for repo, commits in per_repo.items():
        for c in commits or []:
            msg = clean(c["commit"]["message"])
            if not msg or SKIP_MESSAGE.search(msg):
                continue
            rows.append((c["commit"]["author"]["date"], repo, msg, c["html_url"]))
    rows.sort(reverse=True)
    if len(rows) < MIN_COMMITS:
        raise SourceError(f"only {len(rows)} usable commits found, need {MIN_COMMITS}")
    return [f"- {d[:10]} [{repo}]({url}): {msg}" for d, repo, msg, url in rows[:SHOW_COMMITS]]


def build_block(acc, runs, per_repo, now=None):
    now = now or datetime.now(timezone.utc)
    lines = [scoreboard_line(acc), "", pipeline_line(runs), "", "Recent commits:", ""]
    lines += commit_lines(per_repo)
    lines += ["", f"<sub>Refreshed {now.strftime('%Y-%m-%d %H:%M')} UTC by tools/refresh.py.</sub>"]
    return "\n".join(lines)


def collect():
    acc = http_json(ACCURACY_URL)
    runs = gh_json(f"repos/{OWNER}/fpl-decision-engine/actions/workflows/fpl.yml/runs?per_page=1&status=completed")
    per_repo = {r: gh_json(f"repos/{OWNER}/{r}/commits?per_page=15") for r in COMMIT_REPOS}
    return acc, runs, per_repo


def splice(text, block):
    if START not in text or END not in text or text.index(START) > text.index(END):
        raise ValueError("markers missing")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{START}\n{block}\n{END}{tail}"


def main(argv):
    try:
        block = build_block(*collect())
    except SourceError as e:
        print(f"SOURCE FAILED: {e}", file=sys.stderr)
        return 1
    if "--print" in argv:
        print(block)
        return 0
    try:
        new = splice(README.read_text(encoding="utf-8"), block)
    except ValueError as e:
        print(f"README: {e}", file=sys.stderr)
        return 2
    README.write_text(new, encoding="utf-8")
    print("README updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
