from useless_analyzer import UselessAnalyzer
from board_synth import BoardSynth
from fetch_analyzer import FetchAnalyzer
from minimax_soul import MinimaxSoul
from useless_soul import UselessSoul
from electronic_soul import ElectronicSoul
from naive_soul import NaiveSoul
from move_finder import MoveFinder
from points_cache import PointsCache
from clock_it import clock
import click
import os

# number of identical cards and maximum moves allowed in the game
CARDS = 24
MAX_MOVES = 60

p1 = {}
p2 = {}

players = [p1, p2]

# first player (1 or 0)
active = 0
winner = False

# to enable the generation of a trace if required by the game player
def require_trace():
    if click.confirm('Would you like to generate a trace of the minimax?', default=True):
        return True
    return False


# for manual play, prompt the user to choose between dots or colors
# assign other choice to the electronic soul
def get_choice(choices):
    choice = ""
    while choice not in choices:
        choice = input(
            "Welcome to Double Card!\n"
            "Which of [%s] would you like to play as? " % ", ".join(choices))
    return choice


# select choices for players
choice = "colors"
# choice = get_choice(["dots", "colors"])
opp_choice = ""

if choice == "dots":
    opp_choice = "colors"
else:
    opp_choice = "dots"

# prompt to inquire if trace is needed
generate_trace = require_trace()


bs = BoardSynth()
mf = MoveFinder(bs)
ach = PointsCache("analysis.pkl")
ach2 = PointsCache("aggressive_analysis.pkl",
                   our_points={0: 6, 1: 14, 2: 600000},
                   their_points={0: 12, 1: 1000, 2: 20000})
faz = FetchAnalyzer(ach)
faz2 = FetchAnalyzer(ach2)
naive_sl = NaiveSoul(bs, faz, mf)
naive_chaos = NaiveSoul(bs, faz, mf, sanity=77)
monkey = ElectronicSoul(bs, faz, mf, sanity=100)
minimax = MinimaxSoul(bs, faz, mf)
aggressive_minimax = MinimaxSoul(bs, faz2, mf)
minimax_chaos = MinimaxSoul(bs, faz, mf, sanity=77)
ua = UselessAnalyzer()
useless = UselessSoul(bs, ua, mf, True) if generate_trace else UselessSoul(bs, ua, mf, False)

board = bs.new()
all_moves = []
dot_wins = 0
color_wins = 0
meta_moves = []

p1["name"] = "useless"
p1["token"] = choice
p1["soul"] = useless

p2["name"] = "aggressive_minimax"
p2["token"] = opp_choice
p2["soul"] = aggressive_minimax

# the following will fill up the board, helping with the recycle implementation
# all_moves = [['0', '1', 'a', '1'], ['0', '6', 'b', '2'], ['0', '6', 'c', '1'], ['0', '3', 'd', '1'], ['0', '8', 'c', '3'], ['0', '2', 'A', '2'], ['0', '1', 'F', '1'], ['0', '8', 'H', '1'], ['0', '3', 'E', '2'], ['0', '5', 'E', '3'], ['0', '8', 'D', '2'], ['0', '1', 'D', '4'], ['0', '8', 'H', '3'], ['0', '8', 'H', '5'], ['0', '8', 'H', '7'], ['0', '8', 'H', '9'], ['0', '8', 'H', '11'], ['0', '8', 'D', '5'], ['0', '8', 'D', '7'], ['0', '8', 'D', '9'], ['0', '8', 'D', '11'], ['0', '4', 'A', '4'], ['0', '4', 'A', '6']]
# all_moves = [['0', '5', 'a', '1'], ['0', '5', 'a', '2'], ['0', '5', 'a', '3'], ['0', '7', 'a', '4'], ['0', '8', 'a', '5'], ['0', '8', 'b', '5'], ['0', '5', 'c', '1'], ['0', '5', 'c', '2'], ['0', '5', 'c', '3'], ['0', '7', 'c', '4'], ['0', '8', 'c', '5'], ['0', '8', 'd', '5'], ['0', '5', 'e', '1'], ['0', '5', 'e', '2'], ['0', '5', 'e', '3'], ['0', '7', 'e', '4'], ['0', '8', 'e', '5'], ['0', '8', 'f', '5'], ['0', '5', 'g', '1'], ['0', '5', 'g', '2'], ['0', '5', 'g', '3'], ['0', '7', 'g', '4'], ['0', '8', 'g', '5'], ['0', '8', 'h', '5']]
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
        # to allow users to enter input containing spaces
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
    winner = faz.check_victory(board, players[active]['token'])

    if winner:
        if winner == "dots":
            dot_wins = dot_wins + 1
        if winner == "colors":
            color_wins = color_wins + 1
            meta_moves.append(all_moves)
        if color_wins < 0:
            winner = ""
            active = 0
            all_moves = []
            board = bs.new()
            clear()
            bs.render(board)
            continue
        print("Game over,", winner, "win!")
        break

    if len(all_moves) >= MAX_MOVES:
        print("The maximum number of moves has been reached. It is a draw.")
        break

    active = (active + 1) % 2

print("Dot wins: ", dot_wins)
print("Color wins: ", color_wins)
print("Color win games: ")
print(meta_moves)
