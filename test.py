from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
import os

bs = BoardSynth()
baz = BoardAnalyzer()

board = bs.new()
bs.apply(board, '05a1', '02h1', '02g1','08g3', '08f1')
bs.render(board)
baz.analyze(board)

import ipdb; ipdb.set_trace()
