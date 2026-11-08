"""Generate assets/terminal.svg: a self-contained animated terminal window.
No script, no external font or service. Edit LINES, then run: python3 tools/make_terminal.py"""
from xml.sax.saxutils import escape

CMD = "whoami --verbose"
ROWS = [
    ("name", "Percival Mahwaya"),
    ("role", "Data and DevOps engineer"),
    ("where", "Katowice, Poland"),
    ("degree", "MSc Data Science, Akademia WSB, 2026"),
    ("before", "More than half a decade of law-enforcement IT"),
    ("now", "Pivoting to DevOps/cloud engineering"),
    ("stack", "Python, SQL, GitHub Actions, Django"),
    ("open", "Data, DevOps, research. Ireland or Australia."),
]
W, CW, LH, X0, KEYW = 640, 9.6, 26, 28, 8   # width, char width, line height, left pad, key column chars
TOP = 78
TYPE0, PER_CHAR, GAP = 0.6, 0.07, 0.22

VALS = ';'.join(f'{CW*i:.1f}' for i in range(len(CMD)+1))
alt = "Terminal window. Command: " + CMD + ". Output: " + " ".join(f"{k}: {v.rstrip('.')}." for k, v in ROWS)
H = TOP + LH * (len(ROWS) + 2) + 26
t_cmd_end = TYPE0 + PER_CHAR * len(CMD)
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(alt, {chr(34): "&quot;"})}">',
 f'<title>{escape(alt)}</title>',
 '<style>',
 'text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace;font-size:16px;fill:#c9d1d9;white-space:pre}',
 '.k{fill:#7ee787}.p{fill:#79c0ff}.d{fill:#8b949e}.t{font-size:13px;fill:#8b949e}',
 '@keyframes b{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:b 1s steps(1) 6}',
 '@media (prefers-reduced-motion:reduce){.l{visibility:visible!important}.cmd{clip-path:none!important}.cur{animation:none}}',
 '</style>',
 f'<defs><clipPath id="c"><rect x="{X0+2*CW}" y="{TOP-18}" width="0" height="24">'
 f'<animate attributeName="width" begin="{TYPE0}s" dur="{PER_CHAR*len(CMD):.2f}s" values="{VALS}" calcMode="discrete" fill="freeze"/>'
 '</rect></clipPath></defs>',
 f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
 f'<rect width="{W}" height="34" rx="10" fill="#161b22"/><rect y="24" width="{W}" height="10" fill="#161b22"/>',
 '<circle cx="20" cy="17" r="6" fill="#ff5f56"/><circle cx="40" cy="17" r="6" fill="#ffbd2e"/><circle cx="60" cy="17" r="6" fill="#27c93f"/>',
 f'<text class="t" x="{W/2}" y="21" text-anchor="middle">percival@github: ~ (zsh)</text>',
 f'<text x="{X0}" y="{TOP}"><tspan class="k">$</tspan></text>',
]
# typed command: all-chars text clipped by growing rect
n = len(CMD)
out.append(f'<text class="cmd" clip-path="url(#c)" x="{X0+2*CW}" y="{TOP}" textLength="{CW*n:.1f}" lengthAdjust="spacing">{escape(CMD)}</text>')
y = TOP + LH + 6
t = t_cmd_end + 0.35
for k, v in ROWS:
    line = f'<tspan class="p">{escape(k.ljust(KEYW))}</tspan>{escape(v)}'
    out.append(f'<text class="l" visibility="hidden" x="{X0}" y="{y}">{line}<set attributeName="visibility" to="visible" begin="{t:.2f}s" fill="freeze"/></text>')
    y += LH; t += GAP
y += 6
out.append(f'<text class="l" visibility="hidden" x="{X0}" y="{y}"><tspan class="k">$</tspan> <tspan class="cur">&#9608;</tspan><set attributeName="visibility" to="visible" begin="{t:.2f}s" fill="freeze"/></text>')
# cursor shown at the first prompt while typing is not needed; keep it quiet.
out.append('</svg>')
open("assets/terminal.svg", "w").write("\n".join(out))
print("alt:", alt)
