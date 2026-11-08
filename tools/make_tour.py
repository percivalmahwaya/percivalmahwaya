"""Generate assets/knights-tour.svg: an animated knight's tour on a chessboard.
CSS keyframes plus one SMIL motion path. No script, no external resource at
RUN TIME - the knight shape below is copied in once, at generation time, not
fetched live.
Run: python3 tools/make_tour.py"""
S, M, TOP = 44, 28, 14                 # square size, left margin for ranks, top pad
W = M + 8 * S + 14
H = TOP + 8 * S + 22 + 34
STEP, T0 = 0.6, 0.6                    # seconds per move, start delay
MOVES = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]

# Knight glyph: "chessnut" piece set from lichess.org's lila repo
# (github.com/lichess-org/lila, public/piece/chessnut/wN.svg), by Alexis
# Luengas, Apache License 2.0 (github.com/LexLuengas/chessnut-pieces).
# Recoloured from the original white-fill/black-stroke to this file's own
# green-on-dark palette; geometry untouched. Original viewBox 0 0 800 800,
# recentred and scaled down via the wrapping <g transform>, not by editing
# the path data itself.
_KNIGHT_D1 = ("M645.3 692.2V280.6C588 238.8 503 194.8 448.7 182.5c-42.6-9.7-101.3-2.1-148.6 13.2"
              "a96 96 0 0 0-81.5-60.4c6.3 29.6 5.9 74.3 24.3 97.7-7 16.2-32.1 69.4-48.7 119.3v39.4"
              "a5617.5 5617.5 0 0 0-43.4 212.8L271.7 656l22.4-58.1c15.2-22.7 45.7-60.9 65-78.2 24.5-10.3 "
              "55.9-29.4 66.7-59.2 14-38.4 6.3-84.3-10.5-119.9 31 30.2 50 77 50 127.8 0 68.1-38.1 145.9-104.7 "
              "223.7h284.7z")
KNIGHT_PATH = (
    f'<g fill="#7ee787" stroke="#0d1117" stroke-miterlimit="10">'
    f'<path stroke-linecap="round" stroke-width="29.2" d="{_KNIGHT_D1}"/>'
    '<path stroke-width="9.2" d="M179.8 574.8c19.4-10.9 33.9 3.8 22.4 25.2z"/>'
    '<path d="M231.5 357.9c-7 9.5-.6 29.3 6 34.5a50 50 0 0 0 18.6-8l21.5-24.9-4.5-3.7a264 264 0 0 0-41.6 2.1z"/>'
    '<path stroke-linecap="square" stroke-width="23.8" d="M320 186c-12.4-17.9-9.8-49.7 7-75.1a68.2 68.2 0 0 1 35.2 70.6"/>'
    '</g>'
)
KNIGHT_SCALE = 0.045  # ~36 units across, fits inside a 44px square

def tour(start):
    seen = {start}; path = [start]
    def deg(p):
        return sum(1 for dx,dy in MOVES if 0<=p[0]+dx<8 and 0<=p[1]+dy<8 and (p[0]+dx,p[1]+dy) not in seen)
    while len(path) < 64:
        x,y = path[-1]
        nxt = [(x+dx,y+dy) for dx,dy in MOVES if 0<=x+dx<8 and 0<=y+dy<8 and (x+dx,y+dy) not in seen]
        if not nxt: return None
        n = min(nxt, key=lambda p:(deg(p), p))   # Warnsdorff rule
        seen.add(n); path.append(n)
    return path

path = None
for sx in range(8):
    for sy in range(8):
        path = tour((sx,sy))
        if path: break
    if path: break
assert path and len(set(path)) == 64
assert all((abs(a[0]-b[0]),abs(a[1]-b[1])) in ((1,2),(2,1)) for a,b in zip(path,path[1:]))

def c(p):  # square centre; y flipped so rank 1 is at the bottom
    return (M + p[0]*S + S/2, TOP + (7-p[1])*S + S/2)

files = "abcdefgh"
sq = lambda p: f"{files[p[0]]}{p[1]+1}"
alt = (f"Animation of a knight's tour on a chessboard. A knight starts on {sq(path[0])} and visits all 64 squares exactly once "
       f"in 63 moves, ending on {sq(path[-1])}. Each visited square is numbered in order.")
pts = " ".join(f"{x:.1f},{y:.1f}" for x,y in map(c, path))
dur = STEP * 63
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">',
 f'<title>{alt}</title>', '<style>',
 'text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace}',
 '.lab{font-size:11px;fill:#8b949e;text-anchor:middle}.cap{font-size:13px;fill:#8b949e;text-anchor:middle}',
 '.n{font-size:10px;fill:#7ee787;text-anchor:middle;opacity:0;animation:show 0s linear forwards}',
 '@keyframes show{to{opacity:1}}',
 f'.trail{{fill:none;stroke:#7ee787;stroke-width:2;stroke-linejoin:round;stroke-linecap:round;opacity:.55;stroke-dasharray:1000;stroke-dashoffset:1000;animation:draw {dur:.2f}s linear {T0}s forwards}}',
 '@keyframes draw{to{stroke-dashoffset:0}}',
 '@media (prefers-reduced-motion:reduce){.n{opacity:1;animation:none}.trail{stroke-dashoffset:0;animation:none}.knight{display:none}}',
 '</style>',
 f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>']
for x in range(8):
    for y in range(8):
        light = (x+y) % 2 == 1
        o.append(f'<rect x="{M+x*S}" y="{TOP+(7-y)*S}" width="{S}" height="{S}" fill="{"#21262d" if light else "#161b22"}"/>')
for i in range(8):
    o.append(f'<text class="lab" x="{M+i*S+S/2}" y="{TOP+8*S+14}">{files[i]}</text>')
    o.append(f'<text class="lab" x="{M/2}" y="{TOP+(7-i)*S+S/2+4}">{i+1}</text>')
o.append(f'<polyline class="trail" pathLength="1000" points="{pts}"/>')
for i,p in enumerate(path):
    x,y = c(p)
    o.append(f'<text class="n" x="{x-S/2+9:.1f}" y="{y-S/2+13:.1f}" style="animation-delay:{T0+i*STEP:.2f}s">{i+1}</text>')
d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x,y in map(c, path))
o.append(f'<g class="knight" visibility="hidden"><set attributeName="visibility" to="visible" begin="{T0}s" fill="freeze"/>'
         f'<g transform="scale({KNIGHT_SCALE}) translate(-400,-400)">{KNIGHT_PATH}</g>'
         f'<animateMotion path="{d}" begin="{T0}s" dur="{dur:.2f}s" fill="freeze" calcMode="linear"/></g>')
o.append(f'<text class="cap" x="{W/2}" y="{H-12}">Knight\'s tour: 64 squares, once each.</text>')
o.append('</svg>')
open("assets/knights-tour.svg","w").write("\n".join(o))
print("alt:", alt); print("bytes:", len("\n".join(o)))
