from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from analysis_cache import AnalysisCache
from move_finder import MoveFinder
from alpha_lite_soul import AlphaLiteSoul
from points_cache import PointsCache
from clock_it import clock
import os
ach = PointsCache("analysis.pkl")
faz = FetchAnalyzer(ach)
bs = BoardSynth()
mf = MoveFinder(bs)
alhot = AlphaLiteSoul(bs, faz, mf, hotness=1)
aldhot = AlphaLiteSoul(bs, faz, mf, hotness=1)
alnot = AlphaLiteSoul(bs, faz, mf)
aldnot = AlphaLiteSoul(bs, faz, mf)
all_moves = []
board = bs.new()
token = "dots"
move = None

bs.render(board)
for _ in range(10):
    if token == "dots":
        print("AL DHOT")
        move = clock(aldhot.get_move)(board, token, moves_played_count=(len(all_moves)))
        print("AL DNOT")
        move2 = clock(aldnot.get_move)(board, token, moves_played_count=(len(all_moves)))
    else:
        print("AL HOT")
        move = clock(alhot.get_move)(board, token, moves_played_count=(len(all_moves)))
        print("AL NOT")
        move2 = clock(alnot.get_move)(board, token, moves_played_count=(len(all_moves)))
    if move != move2:
        print("Not the same move:",move, move2)
    else:
        print("Final move:",move)
    bs.apply(board, move)
    bs.render(board)
    all_moves.append(move)
    if faz.check_victory(board, "dots"):
        break
    if faz.check_victory(board, "colors"):
        break
    token = "colors" if token == "dots" else "dots"
