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

# blocking the 4 in a row gives enemy 3 in a row anyway
# bs.apply(board, "04d1", "06b1", "08c1", "04d3", "05f1")
# NOT FIXED
# but also: What do?

# not blocking the 4 in a row, gives yourself more points,
# asymmetric heuristics should fix this one
# bs.apply(board, "03c1", "06c2", "08f1", "02e1", "02d2")
# bs.apply(board, "01a1", "06b2", "06c1", "03d1", "08c3")
# FIXED


bs.render(board)
mf = MoveFinder()
es = ElectronicSoul(bs, baz, "naive_single_layer", "dots")
print(es.get_move(board))

import ipdb; ipdb.set_trace()
