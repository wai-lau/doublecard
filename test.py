from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from analysis_cache import AnalysisCache
from move_finder import MoveFinder
from electronic_soul import ElectronicSoul
from clock_it import clock
import os

bs = BoardSynth()
ach = AnalysisCache()
baz = BoardAnalyzer(ach)

board = bs.new()

all_moves = [['0', '5', 'a', '1'], ['0', '5', 'a', '2'], ['0', '5', 'a', '3'], ['0', '7', 'a', '4'], ['0', '7', 'a', '5'], ['0', '7', 'a', '6'], ['0', '5', 'c', '1'], ['0', '5', 'c', '2'], ['0', '5', 'c', '3'], ['0', '7', 'c', '4'], ['0', '7', 'c', '5'], ['0', '7', 'c', '6'], ['0', '5', 'e', '1'], ['0', '5', 'e', '2'], ['0', '5', 'e', '3'], ['0', '7', 'e', '4'], ['0', '7', 'e', '5'], ['0', '7', 'e', '6'], ['0', '5', 'g', '1'], ['0', '5', 'g', '2'], ['0', '5', 'g', '3'], ['0', '7', 'g', '4'], ['0', '7', 'g', '5'], ['0', '7', 'g', '6']]
bs.apply(board, *all_moves)

bs.render(board)
mf = MoveFinder(bs)
es = ElectronicSoul(bs, baz, "naive_single_layer", "dots")
recyclable = clock(mf.find_recyclable)(board, all_moves[-1])
