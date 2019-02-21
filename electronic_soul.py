from random import shuffle, random
from move_finder import MoveFinder

class ElectronicSoul:
    def __init__(self, bs, baz, method):
        self.mf = MoveFinder(bs)
        self.bs = bs
        self.baz = baz
        if method == "naive_single_layer":
            self.method = self.naive_single_layer
            self.recycle = self.naive_single_layer_recycle
        elif method == "chaos_monkey":
            self.method = self.chaos_monkey
            self.recycle = self.chaos_monkey_recycle
        elif method == "chaos_naive":
            self.method = self.chaos_naive
            self.recycle = self.chaos_naive_recycle
        elif method == "minimax":
            self.method = self.minimax

    # for recursive searching, we need to be careful on the transition
    # from regular move to recycling moves
    def get_move(self, board, token, last_move=None, moves_played_count=None):
        if moves_played_count and moves_played_count >= 24:
            return self.recycle(board, token, last_move)
        return self.method(board, token)

    def naive_single_layer(self, board, token):
        possible_moves = self.mf.find_moves(board)
        current = self.baz.analyze(board, token)
        best_move = ''
        best_diff = -500000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            h = self.baz.analyze(b, token)
            if (h - current) > best_diff:
                best_move = m
                best_diff = h - current
        return best_move

    def naive_single_layer_recycle(self, board, token, last_move):
        possible_moves = self.mf.find_recyclable(board, last_move)
        current = self.baz.analyze(board, token)
        best_move = ''
        best_diff = -500000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.recycle(b, m, last_move)
            h = self.baz.analyze(b, token)
            if (h - current) > best_diff:
                best_move = m
                best_diff = h - current
        return best_move

    def chaos_monkey(self, board, token):
        moves = self.mf.find_moves(board)
        shuffle(moves)
        return moves[0]

    def chaos_monkey_recycle(self, board, token, last_move):
        moves = self.mf.find_recyclable(board, last_move)
        shuffle(moves)
        return moves[0]

    def chaos_naive(self, board, token):
        if all(not c[0] for c in board):
            return self.chaos_monkey(board, token)
        if random() * 100 < 33:
            print("CHAOS PLAYS")
            return self.chaos_monkey(board, token)
        else:
            print("-naive- plays")
            return self.naive_single_layer(board, token)

    def chaos_naive_recycle(self, board, token, last_move):
        if random() * 100 < 33:
            print("CHAOS PLAYS")
            return self.chaos_monkey_recycle(board, token, last_move)
        else:
            print("-naive- plays")
            return self.naive_single_layer_recycle(board, token, last_move)

    def flipside(self, token):
        return "dots" if token == "colors" else "dots"
