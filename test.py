from block_cache import BlockCache
from block_analyzer import BlockAnalyzer
from board_synth import BoardSynth
from alpha_lite_soul import AlphaLiteSoul
from move_finder import MoveFinder

bs = BoardSynth()
mf = MoveFinder(bs)
bach = BlockCache("block_analysis.pkl")
baz = BlockAnalyzer(bach)
board = bs.new()
bs.apply(board, [2, 'g', 1], [8, 'E', 1], [4, 'D', 1], [2, 'F', 1], [6, 'H', 1])
         #, [8, 'B', 1])
         # [2, 'F', 1], [2, 'A', 1], [6, 'D', 1])
bs.render(board)
alphalite = AlphaLiteSoul(bs, baz, mf, depth=3, hotness=1)
alphalite.get_move(board, "dots", moves_played_count=5)
import ipdb; ipdb.set_trace()
