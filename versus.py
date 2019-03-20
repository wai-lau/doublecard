from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from move_finder import MoveFinder
from alpha_lite_soul import AlphaLiteSoul
from thick_analyzer import ThickAnalyzer
from thick_cache import ThickCache
from clock_it import clock
import os

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

# number of identical cards and maximum moves allowed in the game
CARDS = 24
MAX_MOVES = 40

# first player (1 or 0)
winner = False

bs = BoardSynth()
mf = MoveFinder(bs)
tach = ThickCache("tach.pkl")
taz = ThickAnalyzer(tach)
game_analyzer = taz
alphalite = AlphaLiteSoul(bs, taz, mf, depth=3, hotness=1)

board = bs.new()

clear()

p1 = {}
p1["name"] = input("What's your name? ")
p1["token"] = "dots" if input("Dots or colors? ").replace("s", "").lower() == "dot" else "colors"
p1["soul"] = "organic"

p2 = {}
p2["name"] = "BLOCKU"
p2["token"] = "colors" if p1["token"] == "dots" else "dots"
p2["soul"] = alphalite

players = [p1, p2] if input("Player (1) or (2)? ") == "1" else [p2, p1]

active = 0
all_moves = []
# the following will fill up the board, helping with the recycle implementation
# all_moves = [["3", "a", "1"],["2","c","1"]]
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

bs.apply(board, *all_moves)

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
            if all_moves:
                move = get_move(players[active], len(all_moves), all_moves[-1])
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
    print()
    winner = game_analyzer.check_victory(board, players[active]['token'])
    if not winner:
        winner = game_analyzer.check_victory(board, players[(active + 1) % 2]['token'])

    if winner:
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
