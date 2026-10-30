#!/usr/bin/env python3
"""Static checks for README.md. Exit 1 on any failure.

1. Markers present and in order.
2. No em dash, no raw email address, no phone number, no "No activity tracked".
3. Every image has non-empty alt text.
4. Every github.com blob or tree link points at a path that exists (uses gh api).
   Skip this one with --offline.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
text = (ROOT / "README.md").read_text(encoding="utf-8")
fails = []

if not (("<!-- latest:start -->" in text) and ("<!-- latest:end -->" in text)
        and text.index("<!-- latest:start -->") < text.index("<!-- latest:end -->")):
    fails.append("latest markers missing or out of order")

for name, pat in {
    "em dash": "—",
    "raw email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "phone number": r"\(?\+\d{1,3}\)?[\s.-]?\d[\d\s.-]{6,}\d|\b\d{3}[ .-]\d{3}[ .-]\d{3}\b",
    "empty-widget text": r"No activity tracked",
}.items():
    # the commit-hash URLs in the Latest block are not phone numbers
    scan = re.sub(r"\(https?://[^)]+\)", "", text) if name == "phone number" else text
    if re.search(pat, scan):
        fails.append(f"found {name}")

for m in re.finditer(r"!\[([^\]]*)\]\(", text):
    if not m.group(1).strip():
        fails.append("image with empty alt text")
for m in re.finditer(r"<img\b[^>]*>", text, re.I):
    if not re.search(r'alt="[^"]+"', m.group(0)):
        fails.append("img tag without alt text")

if "--offline" not in sys.argv:
    seen = set()
    for m in re.finditer(r"https://github\.com/([\w.-]+)/([\w.-]+)/(?:blob|tree)/([\w.-]+)/([^\s)#]+)", text):
        owner, repo, branch, path = m.groups()
        if m.group(0) in seen:
            continue
        seen.add(m.group(0))
        r = subprocess.run(["gh", "api", f"repos/{owner}/{repo}/contents/{path}?ref={branch}", "--jq", ".name"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fails.append(f"missing path: {owner}/{repo}@{branch}:{path}")
    print(f"checked {len(seen)} evidence paths")

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("README checks passed")
