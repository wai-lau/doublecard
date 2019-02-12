from random import shuffle, random
from move_finder import MoveFinder

class ElectronicSoul:
    def __init__(self, bs, baz, method, token):
        self.mf = MoveFinder()
        self.bs = bs
        self.baz = baz
        self.token = token
        if method == "naive_single_layer":
            self.method = self.naive_single_layer
        elif method == "chaos_monkey":
            self.method = self.chaos_monkey
        elif method == "chaos_naive":
            self.method = self.chaos_naive

    def get_move(self, board):
        return self.method(board)

    def naive_single_layer(self, board):
        possible_moves = self.mf.find_moves(board)
        current = self.baz.heuristic(board, self.token)
        best_move = ''
        best_diff = -2000000000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            h = self.baz.heuristic(b, self.token)
            if (h - current) > best_diff:
                best_move = m
                best_diff = h - current
        return best_move

    def chaos_monkey(self, board):
        moves = self.mf.find_moves(board)
        shuffle(moves)
        return moves[0]

    def chaos_naive(self, board):
        if all(not c[0] for c in board):
            return self.chaos_monkey(board)
        if random() * 100 < 33:
            print("CHAOS PLAYS")
            return self.chaos_monkey(board)
        else:
            print("-naive- plays")
            return self.naive_single_layer(board)
