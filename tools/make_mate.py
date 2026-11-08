"""Generate assets/kbn-mate.svg: a REAL, verified King+Bishop+Knight vs King
checkmate, animated on the same board/palette as make_tour.py.

The move sequence is NOT hand-typed from memory - this is the one endgame
where a plausible-but-wrong line is an easy, common mistake (the defending
king must be driven to the corner matching the BISHOP'S square colour;
getting that backwards is the standard beginner error). It was computed with
a small adversarial search against python-chess's own legal-move generator
(see tools/solve_kbn_mate.py, run separately, output pasted into MOVES
below) and is re-verified here, at generation time, by replaying every SAN
move through python-chess and asserting the final position is checkmate.
If that assertion ever fails, this script refuses to generate the image.

Piece art: "chessnut" set from lichess.org's lila repo
(github.com/lichess-org/lila/.../public/piece/chessnut/), by Alexis Luengas,
Apache License 2.0 - same source and licence already used for the knight in
make_tour.py. Geometry copied as-is; only recoloured.

Run: python3 tools/make_mate.py
"""
import sys

sys.path.insert(0, r"C:\Users\Percival Mahwaya\Desktop\bcaChessHub\venv\Lib\site-packages")
import chess  # noqa: E402

START_FEN = "8/8/8/4k3/8/2KBN3/8/8 w - - 0 1"
MOVES = ("Nf5 Kf6 Kd4 Kf7 Ke5 Kf8 Kf6 Ke8 Ng7+ Kd8 Ke6 Kc7 Ne8+ Kb8 Nd6 Ka8 "
         "Kd7 Kb8 Kd8 Ka8 Kc7 Ka7 Nc8+ Ka8 Be4#").split()

S, M, TOP = 44, 28, 14
W = M + 8 * S + 14
H = TOP + 8 * S + 22 + 34
T0 = 0.6
STEP = 2.2       # seconds per ply - "much slower" than the knight's tour
HOP = STEP * 0.85  # the hop itself doesn't fill the whole step (a brief pause between moves)

files = "abcdefgh"


def square_xy(name):
    f = files.index(name[0])
    r = int(name[1]) - 1
    return (M + f * S + S / 2, TOP + (7 - r) * S + S / 2)


# ---- re-derive and VERIFY the move sequence, don't trust the literal above
board = chess.Board(START_FEN)
ply_data = []  # (piece_symbol, from_sq, to_sq, san, is_mate)
for san in MOVES:
    mv = board.parse_san(san)
    assert mv in board.legal_moves, f"illegal move in MOVES: {san}"
    piece = board.piece_at(mv.from_square)
    ply_data.append((piece.symbol(), chess.square_name(mv.from_square),
                      chess.square_name(mv.to_square), san, san.endswith("#")))
    board.push(mv)
assert board.is_checkmate(), "MOVES does not end in checkmate - refusing to generate"
print(f"verified: {len(ply_data)}-ply line ends in checkmate ({board.fen()})")

# ---- per-piece waypoint lists: (ply_index_or_-1_for_start, square)
pieces = {}  # key -> list of (ply, square)
START = {"K": "c3", "B": "d3", "N": "e3", "k": "e5"}
for key, sq in START.items():
    pieces[key] = [(-1, sq)]
for i, (piece, frm, to, san, mate) in enumerate(ply_data):
    pieces[piece].append((i, to))

PIECE_COLOUR = {
    "K": ("#c9d1d9", "#0d1117"), "B": ("#c9d1d9", "#0d1117"), "N": ("#c9d1d9", "#0d1117"),
    "k": ("#161b22", "#7ee787"),
}
PIECE_SCALE = 0.052  # ~42 units across - fills most of a 44px square

# ---- piece glyph paths: "chessnut" (Apache 2.0, see module docstring),
# geometry verbatim from public/piece/chessnut/{wK,wB,wN,bK}.svg, recoloured
# via the two %s placeholders (fill, stroke) rather than editing the path
# data. viewBox for all four is 0 0 800 800.
GLYPH = {
    "N": '<g fill="%s" stroke="%s" stroke-miterlimit="10">'
         '<path stroke-linecap="round" stroke-width="29.2" d="M645.3 692.2V280.6C588 238.8 503 194.8 448.7 182.5'
         'c-42.6-9.7-101.3-2.1-148.6 13.2a96 96 0 0 0-81.5-60.4c6.3 29.6 5.9 74.3 24.3 97.7-7 16.2-32.1 69.4-48.7 119.3v39.4'
         'a5617.5 5617.5 0 0 0-43.4 212.8L271.7 656l22.4-58.1c15.2-22.7 45.7-60.9 65-78.2 24.5-10.3 '
         '55.9-29.4 66.7-59.2 14-38.4 6.3-84.3-10.5-119.9 31 30.2 50 77 50 127.8 0 68.1-38.1 145.9-104.7 '
         '223.7h284.7z"/>'
         '<path stroke-width="9.2" d="M179.8 574.8c19.4-10.9 33.9 3.8 22.4 25.2z"/>'
         '<path d="M231.5 357.9c-7 9.5-.6 29.3 6 34.5a50 50 0 0 0 18.6-8l21.5-24.9-4.5-3.7a264 264 0 0 0-41.6 2.1z"/>'
         '<path stroke-linecap="square" stroke-width="23.8" d="M320 186c-12.4-17.9-9.8-49.7 7-75.1a68.2 68.2 0 0 1 35.2 70.6"/>'
         '</g>',
}

_pieces_dir = None


def load_glyph(src_file, fill, stroke):
    """Read a saved chessnut SVG, strip the outer <svg> wrapper, recolour
    every fill="#fff"/unset-black and stroke, return the inner markup."""
    import re
    text = open(src_file, encoding="utf-8").read()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", text, re.S).group(1)
    # The source files use fill="#fff" for the light piece body and
    # fill="#f2f2f2"/unset(black) + stroke="#f2f2f2"/"#000" for pieces and
    # their outline detail. Recolour both to this file's two-tone scheme
    # rather than try to keep every original internal contrast choice.
    inner = re.sub(r'fill="#fff"', f'fill="{fill}"', inner)
    inner = re.sub(r'stroke="#000"', f'stroke="{stroke}"', inner)
    inner = re.sub(r'stroke="#f2f2f2"', f'stroke="{stroke}"', inner)
    # bK.svg's main body path has no explicit fill (defaults to black) -
    # give it one explicitly so recolouring is total, not partial.
    inner = inner.replace('<path d="M694.7', f'<path fill="{fill}" d="M694.7')
    return inner


def build_pieces_svg(pieces_dir):
    GLYPH["K"] = load_glyph(f"{pieces_dir}/wK.svg", *PIECE_COLOUR["K"])
    GLYPH["B"] = load_glyph(f"{pieces_dir}/wB.svg", *PIECE_COLOUR["B"])
    GLYPH["k"] = load_glyph(f"{pieces_dir}/bK.svg", *PIECE_COLOUR["k"])
    # N above is already recoloured inline (it's short enough to keep
    # readable as a literal, matching make_tour.py's convention); just
    # substitute its two %s colour placeholders now.
    GLYPH["N"] = GLYPH["N"] % PIECE_COLOUR["N"]


if __name__ == "__main__":
    import sys as _sys
    pieces_dir = _sys.argv[1] if len(_sys.argv) > 1 else "tools/_chessnut_pieces"
    build_pieces_svg(pieces_dir)

    total_dur = T0 + len(ply_data) * STEP + 1.5
    alt = (f"Animation of a King, Bishop and Knight checkmating a lone King. "
           f"White plays {', '.join(san for *_, san, _ in ply_data)}. "
           f"Checkmate on move {ply_data[-1][3].rstrip('#')}.")

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">',
         f'<title>{alt}</title>', '<style>',
         'text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace}',
         '.lab{font-size:11px;fill:#8b949e;text-anchor:middle}.cap{font-size:12.5px;fill:#8b949e;text-anchor:middle}',
         '.mv{font-size:13px;fill:#7ee787;text-anchor:middle;font-weight:700}',
         '@media (prefers-reduced-motion:reduce){.piece{visibility:visible!important}.hop{display:none}}',
         '</style>',
         f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>']
    for x in range(8):
        for y in range(8):
            light = (x + y) % 2 == 1
            o.append(f'<rect x="{M+x*S}" y="{TOP+(7-y)*S}" width="{S}" height="{S}" '
                      f'fill="{"#21262d" if light else "#161b22"}"/>')
    for i in range(8):
        o.append(f'<text class="lab" x="{M+i*S+S/2}" y="{TOP+8*S+14}">{files[i]}</text>')
        o.append(f'<text class="lab" x="{M/2}" y="{TOP+(7-i)*S+S/2+4}">{i+1}</text>')

    # One <g class="piece"> per piece, static start position + chained
    # additive animateMotion hops, one per ply that piece actually moves.
    for key, waypoints in pieces.items():
        x0, y0 = square_xy(waypoints[0][1])
        hops = []
        for (ply, sq), (_, prev_sq) in zip(waypoints[1:], waypoints[:-1]):
            x1, y1 = square_xy(sq)
            px, py = square_xy(prev_sq)
            dx, dy = x1 - px, y1 - py
            t = T0 + ply * STEP
            hops.append(f'<animateMotion class="hop" path="M 0,0 L {dx:.3f},{dy:.3f}" '
                         f'begin="{t:.2f}s" dur="{HOP:.2f}s" fill="freeze" additive="sum" calcMode="linear"/>')
        o.append(f'<g class="piece" transform="translate({x0:.1f},{y0:.1f})">'
                  f'<g transform="scale({PIECE_SCALE}) translate(-400,-400)">{GLYPH[key]}</g>'
                  + "".join(hops) + '</g>')

    # Current-move caption: one <text> per ply, shown from its own begin
    # time until the next ply's begin time (or forever, for the last one) -
    # same stacked show/hide technique terminal.svg already uses for rows.
    for i, (piece, frm, to, san, mate) in enumerate(ply_data):
        t_show = T0 + i * STEP
        label = f"{i+1}. {san}" if not mate else f"{i+1}. {san}  CHECKMATE"
        hide = "" if i == len(ply_data) - 1 else (
            f'<set attributeName="visibility" to="hidden" begin="{T0+(i+1)*STEP:.2f}s"/>')
        o.append(f'<text class="mv" x="{W/2}" y="{H-12}" visibility="hidden">{label}'
                  f'<set attributeName="visibility" to="visible" begin="{t_show:.2f}s" fill="freeze"/>'
                  f'{hide}</text>')
    o.append(f'<text class="cap" x="{W/2}" y="{H-12}" visibility="hidden">'
              'King, Bishop and Knight force mate.'
              f'<set attributeName="visibility" to="visible" begin="0s"/>'
              f'<set attributeName="visibility" to="hidden" begin="{T0:.2f}s"/></text>')

    o.append('</svg>')
    open("assets/kbn-mate.svg", "w", encoding="utf-8").write("\n".join(o))
    print("alt:", alt)
    print("total runtime:", f"{total_dur:.1f}s")
    print("bytes:", len("\n".join(o)))
