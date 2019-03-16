from block_cache import BlockCache
from block_analyzer import BlockAnalyzer
from board_synth import BoardSynth
from alpha_lite_soul import AlphaLiteSoul
from line_cache import LineCache
from thick_cache import ThickCache
from block_cache import BlockCache
from move_finder import MoveFinder
from clock_it import clock
from multiprocessing import Process, Value, Array

def f():
    pass

p = clock(Process)(target=f, args=())

