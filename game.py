from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
import os

bs = BoardSynth()
baz = BoardAnalyzer()

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
game_over = False

board = bs.new()

def get_move(player):
    if player["soul"] == "organic":
        move = input("{}'s move: ".format(player["name"]))
        return move
    else:
        print("Ｅｌｅｃｔｒｏｎｉｃ　Ｓｏｕｌ　ｎｏｔ　Ｉｍｐｌｅｍｅｎｔｅｄ")
        exit()

while not game_over:
    os.system('clear')
    bs.render(board)
    baz.analyze(board)
    while True:
        if bs.apply(board, get_move(players[active])):
            break
    active = (active+1)%2

