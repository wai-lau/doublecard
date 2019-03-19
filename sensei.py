from board_synth import BoardSynth
from move_finder import MoveFinder
from alpha_lite_soul import AlphaLiteSoul
from thick_analyzer import ThickAnalyzer
from thick_cache import ThickCache

bs = BoardSynth()
mf = MoveFinder(bs)
tach = ThickCache("tach.pkl")
taz = ThickAnalyzer(tach)

sensei = AlphaLiteSoul(bs, taz, mf, depth=3, sensei=False, hotness=1)

board = bs.new()
bs.apply(board, [1,"C",1])
possible_moves = mf.find_moves(board)
for m in possible_moves:
    board = bs.new()
    bs.apply(board, [1,"C",1])
    bs.apply(board, m)
    dmove = sensei.get_move(board, "dots", moves_played_count=1)
    cmove = sensei.get_move(board, "colors", moves_played_count=1)
    print("\""+"".join(map(str, m))+"\":","[",dmove,",",cmove,"],")
