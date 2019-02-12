from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from analysis_cache import AnalysisCache
from electronic_soul import ElectronicSoul
from clock_it import clock
import os
import re

# number of identical cards and maximum moves allowed in the game
CARDS = 24
MAX_MOVES = 60

# if not manual play, insert the following as default token in below ElectronicSoul instances
NAIVE_DEFAULT = "dots"
MONKEY_DEFAULT = "colors"

p1 = {}
p2 = {}

players = [p1, p2]

# first player (1 or 0)
active = 0
winner = False


# for manual play, prompt the user to choose between dots or colors
# assign other choice to the electronic soul
def get_choice(choices):
    choice = ""
    while choice not in choices:
        choice = input(
            "Welcome to Double Card!\n" +  
            "Which of [%s] would you like to play as? " % ", ".join(choices))
    return choice


choice = get_choice(["dots", "colors"])
opp_choice = ""

if choice == "dots":
    opp_choice == "colors"
else:
    opp_choice = "dots"

bs = BoardSynth()
board = bs.new()
ach = AnalysisCache()
baz = BoardAnalyzer(ach)
naive_sl = ElectronicSoul(bs, baz, "naive_single_layer", opp_choice)
monkey = ElectronicSoul(bs, baz, "chaos_monkey", opp_choice)
all_moves = []

p1["name"] = "PLAYER ONE"
p1["token"] = choice
p1["soul"] = "organic"

p2["name"] = "-naive-"
p2["token"] = opp_choice
p2["soul"] = "organic"


def get_move(player):
    move = ""
    if player["soul"] == "organic":
        move = input("{}, {}'s move: "
                     .format(player["token"], player["name"]))
        # to allow users to enter input containing spaces or different caps
        move = move.split(' ')
    else:
        move = clock(player["soul"].get_move)(board)
        print("{}, {}'s move: {}"
              .format(player["token"], player["name"], move))
        input("Press enter.")
    return move


os.system('clear')
# the following will fill up the board, helping with the recycle implementation
# all_moves = [['0', '1', 'a', '1'], ['0', '6', 'b', '2'], ['0', '6', 'c', '1'], ['0', '3', 'd', '1'], ['0', '8', 'c', '3'], ['0', '2', 'A', '2'], ['0', '1', 'F', '1'], ['0', '8', 'H', '1'], ['0', '3', 'E', '2'], ['0', '5', 'E', '3'], ['0', '8', 'D', '2'], ['0', '1', 'D', '4'], ['0', '8', 'H', '3'], ['0', '8', 'H', '5'], ['0', '8', 'H', '7'], ['0', '8', 'H', '9'], ['0', '8', 'H', '11'], ['0', '8', 'D', '5'], ['0', '8', 'D', '7'], ['0', '8', 'D', '9'], ['0', '8', 'D', '11'], ['0', '4', 'A', '4'], ['0', '4', 'A', '6'], ['0', '4', 'A', '8']]
# bs.apply(board, ['0', '1', 'a', '1'], ['0', '6', 'b', '2'], ['0', '6', 'c', '1'], ['0', '3', 'd', '1'], ['0', '8', 'c', '3'], ['0', '2', 'A', '2'], ['0', '1', 'F', '1'], ['0', '8', 'H', '1'], ['0', '3', 'E', '2'], ['0', '5', 'E', '3'], ['0', '8', 'D', '2'], ['0', '1', 'D', '4'], ['0', '8', 'H', '3'], ['0', '8', 'H', '5'], ['0', '8', 'H', '7'], ['0', '8', 'H', '9'], ['0', '8', 'H', '11'], ['0', '8', 'D', '5'], ['0', '8', 'D', '7'], ['0', '8', 'D', '9'], ['0', '8', 'D', '11'], ['0', '4', 'A', '4'], ['0', '4', 'A', '6'], ['0', '4', 'A', '8'])
bs.render(board)

while not winner:
	# ensure number of moves has not exceeded maximum limit
    if len(all_moves) >= MAX_MOVES:
    	winner = "the maximum number of moves have been reached. It is a draw, you both"
    	break
    while True:
        move = get_move(players[active])
        if len(all_moves) >= CARDS:
            to_remove = move[0:4]
            to_apply = move[4:]
            if bs.recycle(board, to_remove, to_apply, all_moves[-1]):
                all_moves.append(to_apply)
                break
        else:
            if bs.apply(board, move):
                all_moves.append(move)
                break
    # to get a visual trace after each move (for the demo)
    os.system('clear')
    bs.render(board)
    winner = baz.check_victory(board)
    if winner:
        if winner == "active":
            winner = players[active]['token']
        break
    active = (active + 1) % 2

print("Game over,", winner, "win!")
print("Moves played:", all_moves)
