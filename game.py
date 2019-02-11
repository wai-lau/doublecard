from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from analysis_cache import AnalysisCache
from electronic_soul import ElectronicSoul
from clock_it import clock
import os

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

# for manual play, prompt the user to choose between dots or colors and assign the
# other choice to the electronic soul
def get_choice(choices):
  choice = ""
  while choice not in choices:
      choice = input("Which of [%s] would you like to play as? " % ", ".join(choices))
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
# to keep track of the number of moves)
move_count = len(all_moves)

p1["name"] = "PLAYER ONE"
p1["token"] = choice
p1["soul"] = "organic"

p2["name"] = "-naive-"
p2["token"] = opp_choice
p2["soul"] = naive_sl

def get_move(player):
    move = ""
    if player["soul"] == "organic":
        move = input("{}, {}'s move: "
                     .format(player["token"], player["name"]))
    else:
        move = clock(player["soul"].get_move)(board)
        print("{}, {}'s move: {}"
              .format(player["token"], player["name"], move))
        input("Press enter.")
    return move

os.system('clear')
# The following will fill up the board, helping with the recycle implementation
# bs.apply(board, "01a1", "06b2", "06c1", "03d1", "08c3",'02A2', '01F1', '08H1', '03E2', '05E3', '08D2','01D4', '08H3', '08H5', '08H7', '08H9', '08H11', '08D5', '08D7', '08D9', '08D11', '04A4', '04A6')
bs.render(board)

while not winner:
    while True:
        move = get_move(players[active])
        if bs.apply(board, move):
            break
    all_moves.append(move)
    os.system('clear')
    bs.render(board)
    winner = baz.check_victory(board)
    if winner:
        if winner == "active":
            winner = players[active]['token']
        break
    active = (active+1)%2

print("Game over,", winner, "win!")
print("Moves played:", all_moves)
