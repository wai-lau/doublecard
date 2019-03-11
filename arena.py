from datetime import datetime
from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from minimax_soul import MinimaxSoul
from naive_soul import NaiveSoul
from move_finder import MoveFinder
from line_cache import LineCache
from alpha_beta_soul import AlphaBetaSoul
from alpha_lite_soul import AlphaLiteSoul
from clock_it import clock
import os

CARDS = 24
MAX_MOVES = 60

bs = BoardSynth()
mf = MoveFinder(bs)

ach = LineCache("analysis.pkl")
faz = FetchAnalyzer(ach)

ach2 = LineCache("old_analysis.pkl",
                   our_points={0:2, 1:12, 2:600000},
                   their_points={0:12, 1:1000, 2:20000})
faz2 = FetchAnalyzer(ach2)

###################################################################
challenger = AlphaLiteSoul(bs, faz, mf, depth=2, hotness=1)
###################################################################

###################################################################
gatepkeepers = [
   NaiveSoul(bs, faz2, mf),
   MinimaxSoul(bs, faz, mf),
   MinimaxSoul(bs, faz2, mf)
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

possible_moves = mf.find_moves(bs.new())
# remove card reflections and board reflections
possible_moves = possible_moves[:int(len(possible_moves)/2 + 1):2]
best_of = len(possible_moves)

for n, g in enumerate(gatepkeepers):
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
            if delay >= 3500:
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
                    print("(",dot_wins,":",color_wins,")",
                          p2["name"], "lost to",
                          p1["name"], "with seed", m, "\n\n")
                if dot_wins > (best_of*3)/4:
                    print("You have passed this trial.\n\n")
                    passed = True
                if color_wins >= (best_of*1)/4:
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

