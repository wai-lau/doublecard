from board_synth import BoardSynth
from board_analyzer import BoardAnalyzer
from analysis_cache import AnalysisCache
from move_finder import MoveFinder
from clock_it import clock
import os

bs = BoardSynth()

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

board = bs.new()
ach = AnalysisCache()
baza = BoardAnalyzer(ach)
mf = MoveFinder()
all_moves = []

def get_move(player):
    move = ""
    if player["soul"] == "organic":
        move = input("{}, {}'s move: ".format(player["token"], player["name"]))
    else:
        print("{}, {}'s move: \r".format(player["token"], player["name"]), end='')
        possible_moves = mf.find_moves(board)
        best_move = ''
        heuristic = -1 if player["token"] == "dots" else 1
        for m in possible_moves:
            b = bs.copy(board)
            bs.apply(b, m)
            h = baza.heuristic(b)
            if player["token"] == "dots":
                if heuristic < h:
                    best_move = m
                    heuristic = h
            else:
                if heuristic > h:
                    best_move = m
                    heuristic = h
        print("{}, {}'s move: {}".format(player["token"], player["name"], best_move))
        move = best_move
    all_moves.append(move)
    return move

os.system('clear')
bs.render(board)
while not winner:
    while True:
        if players[active]["soul"] != "organic":
            if bs.apply(board, clock(get_move)(players[active])):
                input("\n Press <Enter>.")
                break
        else:
            if bs.apply(board, get_move(players[active])):
                break
    os.system('clear')
    bs.render(board)
    winner = baza.check_victory(board)
    if winner:
        if winner == "active":
            winner = players[active]['token']
        break
    active = (active+1)%2

print("Game over,", winner, "win!")
print("Moves played:", all_moves)
