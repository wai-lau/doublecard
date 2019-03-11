from useless_analyzer import UselessAnalyzer
from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from minimax_soul import MinimaxSoul
from useless_soul import UselessSoul
from electronic_soul import ElectronicSoul
from naive_soul import NaiveSoul
from move_finder import MoveFinder
from points_cache import PointsCache
from alpha_beta_soul import AlphaBetaSoul
from alpha_lite_soul import AlphaLiteSoul
from clock_it import clock
import os

# number of identical cards and maximum moves allowed in the game
CARDS = 24
MAX_MOVES = 60

# first player (1 or 0)
active = 0
winner = False

bs = BoardSynth()
mf = MoveFinder(bs)
ach = PointsCache("analysis.pkl")
ach2 = PointsCache("aggressive_analysis.pkl",
                   our_points={0: 6, 1: 14, 2: 600000},
                   their_points={0: 12, 1: 1000, 2: 20000})
faz = FetchAnalyzer(ach)
faz2 = FetchAnalyzer(ach2)
game_analyzer = faz
naive_sl = NaiveSoul(bs, faz, mf)
naive_chaos = NaiveSoul(bs, faz, mf, sanity=77)
minimax = MinimaxSoul(bs, faz, mf)
aggressive_minimax = MinimaxSoul(bs, faz2, mf)
minimax_chaos = MinimaxSoul(bs, faz, mf, sanity=77)
alphabeta = AlphaBetaSoul(bs, faz, mf, sanity=99)
alphalite = AlphaLiteSoul(bs, faz2, mf, depth=2)

board = bs.new()
all_moves = []
dot_wins = 0
color_wins = 0
meta_moves = []

p1 = {}
p1["name"] = "organic"
p1["token"] = "dots"
p1["soul"] = "organic"

p2 = {}
p2["name"] = "alphalite"
p2["token"] = "colors"
p2["soul"] = alphalite

players = [p1, p2]

# the following will fill up the board, helping with the recycle implementation
# all_moves = [
#     ['0', '1', 'a', '1'],
#     ['0', '1', 'a', '2'],
#     ['0', '3', 'a', '3'],
#     ['0', '3', 'a', '4'],
#     ['0', '3', 'a', '5'],
#     ['0', '1', 'a', '6'],
#     ['0', '1', 'a', '7'],
#     ['0', '3', 'a', '8'],
#     ['0', '1', 'a', '9'],
#     ['0', '3', 'a', '10'],
#     ['0', '3', 'a', '11'],
#     ['0', '3', 'a', '12'],
#     ['0', '3', 'g', '1'],
#     ['0', '3', 'g', '2'],
#     ['0', '1', 'g', '3'],
#     ['0', '1', 'g', '4'],
#     ['0', '1', 'g', '5'],
#     ['0', '3', 'g', '6'],
#     ['0', '3', 'g', '7'],
#     ['0', '1', 'g', '8'],
#     ['0', '3', 'g', '9'],
#     ['0', '1', 'g', '10'],
#     ['0', '3', 'g', '11'],
# ]
# bs.apply(board, *all_moves)

def get_move(player, moves_played_count=None, last_move=None):
    move = ""
    if player["soul"] == "organic":
        move = input("{}: {}, {}'s move: "
                     .format(len(all_moves)+1, player["token"], player["name"]))
        move = move.split(' ')
    else:
        move = clock(player["soul"].get_move)(
            board, player["token"], last_move, moves_played_count)
        print("{}: {}, {}'s move: {}"
              .format(len(all_moves)+1, player["token"], player["name"], move))
        input("Press Enter.")
    return move


def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

clear()
bs.render(board)
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
    clear()
    bs.render(board)
    print("\n"+players[active]["token"],"analysis:",
          game_analyzer.analyze(board, players[active]["token"]))
    print(players[(active + 1) % 2]["token"],"analysis:",
          game_analyzer.analyze(board, players[(active + 1) % 2]["token"]))
    winner = faz.check_victory(board, players[active]['token'])
    if not winner:
        winner = faz.check_victory(board, players[(active + 1) % 2]['token'])

    if winner:
        if winner == "dots":
            dot_wins = dot_wins + 1
        if winner == "colors":
            color_wins = color_wins + 1
        if players[0]["token"] == winner:
            print("\n==>", players[0]["name"], "wins!\n")
        else:
            print("\n==>", players[1]["name"], "wins!\n")
        break

    if len(all_moves) >= MAX_MOVES:
        print("The maximum number of moves has been reached. It is a draw.")
        break

    active = (active + 1) % 2

print(all_moves)
