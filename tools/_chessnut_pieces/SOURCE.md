# Source

Copied verbatim from `github.com/lichess-org/lila`,
`public/piece/chessnut/{wK,wB,wN,bK}.svg`.

Author: Alexis Luengas (github.com/LexLuengas/chessnut-pieces)
License: Apache License 2.0 (github.com/LexLuengas/chessnut-pieces/blob/master/LICENSE.txt)

Geometry unmodified. `tools/make_mate.py` reads these files directly and
recolours them (see `load_glyph()`) - the path data itself is never
hand-retyped, to avoid the transcription-corruption risk that applies to
any long SVG path copied by hand.
