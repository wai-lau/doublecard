from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from analysis_cache import AnalysisCache
from move_finder import MoveFinder
from electronic_soul import ElectronicSoul
from clock_it import clock
from useless_analyzer import UselessAnalyzer
import os

bs = BoardSynth()
board = bs.new()

all_moves = [
    ['0', '3', 'a', '1'],
    ['0', '5', 'a', '2'],
    ['0', '8', 'c', '1'],
    ['0', '8', 'd', '1'],
    ['0', '3', 'e', '1'],
    ['0', '3', 'e', '2'],
    ['0', '1', 'e', '3'],
    ['0', '4', 'c', '3'],
    ['0', '4', 'd', '3']
]
bs.apply(board, *all_moves)
bs.render(board)

ua = UselessAnalyzer()
print(ua.analyze(board, "dots"))

import ipdb; ipdb.set_trace()
