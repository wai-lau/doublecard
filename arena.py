from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from minimax_soul import MinimaxSoul
from naive_soul import NaiveSoul
from move_finder import MoveFinder
from points_cache import PointsCache
from alpha_beta_soul import AlphaBetaSoul
from alpha_lite_soul import AlphaLiteSoul
import os

CARDS = 24
MAX_MOVES = 60

bs = BoardSynth()
mf = MoveFinder(bs)

ach = PointsCache("analysis.pkl")
faz = FetchAnalyzer(ach)

ach2 = PointsCache("aggressive_analysis.pkl",
                   our_points={0:6, 1:14, 2:600000},
                   their_points={0:12, 1:1000, 2:20000})
faz2 = FetchAnalyzer(ach2)

###################################################################
challenger = AlphaLiteSoul(bs, faz, mf)
best_of = 30
###################################################################

###################################################################
gatekeepers = [
    NaiveSoul,
    MinimaxSoul,
    AlphaBetaSoul
]
###################################################################

def get_move(player, moves_played_count=None, last_move=None):
    return player["soul"].get_move(board, player["token"], last_move, moves_played_count)

p1 = {}
p2 = {}

p1["token"] = "colors"
p2["token"] = "dots"
p2["soul"] = challenger

players = [p1, p2]

for g in gatekeepers:
    for n, az in enumerate([faz2, faz]):
        dot_wins = 0
        color_wins = 0
        winner = False
        active = 0
        all_moves = []
        board = bs.new()
        p1["soul"] = g(bs, az, mf, sanity=99)
        keeper = type(p1["soul"]).__name__ + str(n)
        print("You are now facing", keeper)
        while not winner:
            while True:
                if len(all_moves) >= CARDS:
                    move = get_move(players[active], len(all_moves), all_moves[-1])
                    if bs.recycle(board, move, all_moves[-1]):
                        all_moves.append(move)
                        break
                else:
                    move = get_move(players[active], len(all_moves))
                    if bs.apply(board, move):
                        all_moves.append(move)
                        break
            winner = faz.check_victory(board, players[active]['token'])
            if not winner:
                winner = faz.check_victory(board, players[(active + 1) % 2]['token'])

            if winner:
                bs.render(board)
                print(all_moves,"\n")
                if winner == "dots":
                    dot_wins = dot_wins + 1
                    print("(",dot_wins,":",color_wins,")",
                          "Challenger", "decimated",
                          keeper, "\n\n")
                if winner == "colors":
                    color_wins = color_wins + 1
                    print("(",dot_wins,":",color_wins,")",
                          "Challenger", "lost to",
                          keeper, "\n\n")
                if dot_wins < best_of/2:
                    winner = False
                    active = 1
                    all_moves = []
                    board = bs.new()
                else:
                    print("You have passed this trial.\n")
                    break
                if color_wins >= best_of/2:
                    print("Win rate:","(",dot_wins,":",color_wins,")",
                          "versus", keeper,
                          "\n\nYou shall not pass.")
                    exit()

            if len(all_moves) >= MAX_MOVES:
                print("The maximum number of moves has been reached. It is a draw.")
                winner = False
                active = 1
                all_moves = []
                board = bs.new()
                continue

            active = (active + 1) % 2

print("You have passed all the trials. You may now enter the realm of the real.")

