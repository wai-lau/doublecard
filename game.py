from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from clock_it import clock
from analysis_cache import AnalysisCache
import os

bs = BoardSynth()

p1 = {}
p2 = {}

p1["name"] = "Jill Doe"
p1["token"] = "colors"
p1["soul"] = "organic"

p2["name"] = "Jane Doe"
p2["token"] = "dots"
p2["soul"] = "organic"

players = [p1, p2]

# first player (1 or 0)
active = 0
winner = False

board = bs.new()
ach = AnalysisCache()
baza = BoardAnalyzer(ach)
baz = BoardAnalyzer()

def get_move(player):
    if player["soul"] == "organic":
        move = input("{}'s move: ".format(player["name"]))
        return move
    else:
        print("Ｅｌｅｃｔｒｏｎｉｃ　Ｓｏｕｌ　ｎｏｔ　Ｉｍｐｌｅｍｅｎｔｅｄ")
        exit()

while not winner:
    os.system('clear')
    bs.render(board)
    winner = clock(baz.analyze, 100)(board)

    clock(baza.analyze, 100)(board)
    clock(baza.analyze, 100)(board)
    clock(baz.analyze, 100)(board)
    clock(baz.analyze, 100)(board)
    if winner:
        if winner == "active":
            winner = players[active]['token']
        break

    while True:
        if bs.apply(board, get_move(players[active])):
            break
    active = (active+1)%2

print("Game over,", winner, "win!")
