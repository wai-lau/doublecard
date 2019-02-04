from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from analysis_cache import AnalysisCache
from electronic_soul import ElectronicSoul
from clock_it import clock
import os


p1 = {}
p2 = {}

p1["name"] = "PLAYER ONE"
p1["token"] = "colors"
p1["soul"] = "organic"

p2["name"] = "ELECTRONIC SOUL"
p2["token"] = "dots"
p2["soul"] = "electronic"

players = [p1, p2]

# first player (1 or 0)
active = 0
winner = False

bs = BoardSynth()
board = bs.new()
ach = AnalysisCache()
baz = BoardAnalyzer(ach)
esoul = ElectronicSoul(bs, baz, "dots")
all_moves = []

def get_move(player):
    move = ""
    if player["soul"] == "organic":
        move = input("{}, {}'s move: ".format(player["token"], player["name"]))
    else:
        move = esoul.get_move(board)
        print("{}, {}'s move: {}".format(player["token"], player["name"], move))
    all_moves.append(move)
    return move

os.system('clear')
bs.render(board)
while not winner:
    while True:
        if players[active]["soul"] != "organic":
            if bs.apply(board, clock(get_move)(players[active])):
                input("\nPress <Enter>")
                break
        else:
            if bs.apply(board, get_move(players[active])):
                break
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
