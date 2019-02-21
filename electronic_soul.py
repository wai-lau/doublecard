from random import shuffle, random
from move_finder import MoveFinder

class ElectronicSoul:
    def __init__(self, bs, baz, method, token):
        self.mf = MoveFinder(bs)
        self.bs = bs
        self.baz = baz
        self.token = token
        if method == "naive_single_layer":
            self.method = self.naive_single_layer
            self.recycle = self.naive_single_layer_recycle
        elif method == "chaos_monkey":
            self.method = self.chaos_monkey
            self.recycle = self.chaos_monkey_recycle
        elif method == "chaos_naive":
            self.method = self.chaos_naive
            self.recycle = self.chaos_naive_recycle

    # for recursive searching, we need to be careful on the transition
    # from regular move to recycling moves
    def get_move(self, board, last_move, moves_played_count):
        if moves_played_count >= 24:
            return self.recycle(board, last_move)
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

    def naive_single_layer_recycle(self, board, last_move):
        possible_moves = self.mf.find_recyclable(board, last_move)
        current = self.baz.heuristic(board, self.token)
        best_move = ''
        best_diff = -2000000000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.recycle(b, m, last_move)
            h = self.baz.heuristic(b, self.token)
            if (h - current) > best_diff:
                best_move = m
                best_diff = h - current
        return best_move

    def chaos_monkey(self, board):
        moves = self.mf.find_moves(board)
        shuffle(moves)
        return moves[0]

    def chaos_monkey_recycle(self, board, last_move):
        moves = self.mf.find_recyclable(board, last_move)
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

    def chaos_naive_recycle(self, board, last_move):
        if random() * 100 < 33:
            print("CHAOS PLAYS")
            return self.chaos_monkey_recycle(board, last_move)
        else:
            print("-naive- plays")
            return self.naive_single_layer_recycle(board, last_move)
