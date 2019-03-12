from block_cache import BlockCache
from block_analyzer import BlockAnalyzer
from board_synth import BoardSynth
bs = BoardSynth()
bach = BlockCache("block_analysis.pkl")
baz = BlockAnalyzer(bach)
board = bs.new()
bs.apply(board, [7, 'A', 1], [2, 'B', 2])
         #, [8, 'B', 1])
         # [2, 'F', 1], [2, 'A', 1], [6, 'D', 1])
bs.render(board)
print(baz.analyze(board, "dots"))
import ipdb; ipdb.set_trace()
