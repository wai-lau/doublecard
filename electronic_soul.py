from random import shuffle
from move_finder import MoveFinder

class ElectronicSoul:
    def __init__(self, bs, baz, method, token='dots'):
        self.mf = MoveFinder()
        self.bs = bs
        self.baz = baz
        self.token = 'dots'
        if method == "naive_single_layer":
            self.method = self.naive_single_layer
        elif method == "chaos_monkey":
            self.method = self.chaos_monkey

    def get_move(self, board):
        return self.method(board)

    def naive_single_layer(self, board):
        possible_moves = self.mf.find_moves(board)
        best_move = ''
        heuristic = -1 if self.token == "dots" else 1
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            h = self.baz.heuristic(b)
            if self.token == "dots":
                if heuristic < h:
                    best_move = m
                    heuristic = h
            else:
                if heuristic > h:
                    best_move = m
                    heuristic = h

        return best_move

    def chaos_monkey(self, board):
        moves = self.mf.find_moves(board)
        shuffle(moves)
        return moves[0]
