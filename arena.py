from datetime import datetime
from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from minimax_soul import MinimaxSoul
from naive_soul import NaiveSoul
from move_finder import MoveFinder
from line_cache import LineCache
from alpha_lite_soul import AlphaLiteSoul
from block_cache import BlockCache
from block_analyzer import BlockAnalyzer
from thick_analyzer import ThickAnalyzer
from thick_cache import ThickCache
from clock_it import clock
import os

CARDS = 24
MAX_MOVES = 60

bs = BoardSynth()
mf = MoveFinder(bs)

ach = LineCache("analysis.pkl")
faz = FetchAnalyzer(ach)

bach = BlockCache("block_analysis.pkl")
baz = BlockAnalyzer(bach)

tach = ThickCache("tach.pkl")
taz = ThickAnalyzer(tach)

###################################################################
challenger = AlphaLiteSoul(bs, taz, mf, depth=3, hotness=1)
###################################################################

###################################################################
gatekeepers = [
   # MinimaxSoul(bs, faz, mf, depth=2),
   AlphaLiteSoul(bs, taz, mf, depth=1, hotness=1),
]
###################################################################

def get_move(player, moves_played_count=None, last_move=None):
    return player["soul"].get_move(board, player["token"], last_move, moves_played_count)

p1 = {}
p2 = {}

p1["token"] = "colors"

p2["name"] = "Challenger"
p2["token"] = "dots"
p2["soul"] = challenger

players = [p1, p2]

p_moves = mf.find_moves(bs.new())
# remove card reflections and board reflections
possible_moves = p_moves[int(len(p_moves)/2 + 3)::2]
possible_moves += p_moves[:int(len(p_moves)/2 + 4):2]
# try a specific starting position
# possible_moves =[[3, 'B', 1], [3, 'F', 1], [7, 'F', 1], [2, 'G', 1], [6, 'G', 1]]
best_of = len(possible_moves)

cool_gatekeeper_moves = []
for n, g in enumerate(gatekeepers):
    dot_wins = 0
    color_wins = 0
    p1["soul"] = g
    p1["name"] = type(p1["soul"]).__name__ + "#" + str(n)
    print("Challenger is now facing", p1["name"])
    passed = False
    for m in possible_moves:
        winner = False
        active = 1
        board = bs.new()
        all_moves = [m]
        bs.apply(board, m)
        while not winner:
            dt = datetime.now()
            while True:
                if len(all_moves) >= CARDS:
                    print(players[active]["name"]+"'s move: ", end="")
                    move = clock(get_move)(players[active], len(all_moves), all_moves[-1])
                    if bs.recycle(board, move, all_moves[-1]):
                        all_moves.append(move)
                        break
                else:
                    print(players[active]["name"]+"'s move: ", end="")
                    move = clock(get_move)(players[active], len(all_moves))
                    if bs.apply(board, move):
                        all_moves.append(move)
                        break
            dt2 = datetime.now()
            delay = round((dt2-dt).seconds*1000 + (dt2-dt).microseconds/1000, 3)
            if delay >= 6000:
                print("\t========================================================")
                print("\t"+players[active]["name"], "took", delay, "seconds analyzing.")
                print("\tMoves thus far:", all_moves)
                print("\t========================================================")
            winner = faz.check_victory(board, players[active]['token'])
            if not winner:
                winner = faz.check_victory(board, players[(active + 1) % 2]['token'])

            if winner:
                bs.render(board)
                print(all_moves,"\n")
                if winner == "dots":
                    dot_wins = dot_wins + 1
                    print("(",dot_wins,":",color_wins,")",
                          p2["name"], "decimated",
                          p1["name"], "with seed", m, "\n\n")
                if winner == "colors":
                    color_wins = color_wins + 1
                    cool_gatekeeper_moves.append(m)
                    print("Cool gatekeeper moves",cool_gatekeeper_moves)
                    print("(",dot_wins,":",color_wins,")",
                          p2["name"], "lost to",
                          p1["name"], "with seed", m, "\n\n")
                if dot_wins >= best_of:
                    print("You have passed this trial.\n\n")
                    passed = True
                if color_wins >= best_of:
                    print("Win rate:","(",dot_wins,":",color_wins,")",
                          "versus", p1["name"],
                          "\n\nYou shall not pass.")
                    exit()

            if len(all_moves) >= MAX_MOVES:
                print("The maximum number of moves has been reached. It is a draw.")

            active = (active + 1) % 2
        if passed:
            break

print("You have passed all the trials. You may now enter the realm of the real.")
