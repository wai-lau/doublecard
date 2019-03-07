import os
from random import shuffle, random

class ElectronicSoul:
    def __init__(self, bs, baz, method, mf):
        self.mf = mf
        self.bs = bs
        self.baz = baz
        if method == "naive_single_layer":
            self.method = self.naive_single_layer
            self.recycle = self.naive_single_layer_recycle
        elif method == "chaos_monkey":
            self.method = self.chaos_monkey
            self.recycle = self.chaos_monkey_recycle
        elif method == "chaos_naive":
            self.method = self.chaos(self.naive_single_layer)
            self.recycle = self.chaos(self.naive_single_layer_recycle, True)
        elif method == "minimax":
            self.method = self.minimax
            self.recycle = self.minicycle
        elif method == "chaos_minimax":
            self.method = self.chaos(self.minimax)
            self.recycle = self.chaos(self.minicycle, True)

    # for recursive searching, we need to be careful on the transition
    # from regular move to recycling moves
    def get_move(self, board, token, last_move=None, moves_played_count=None):
        if moves_played_count and moves_played_count >= 24:
            return self.recycle(board, token, last_move)
        return self.method(board, token, moves_played_count)

    def minimax(self, board, token, moves_played_count, *args):
        return self.m_search(board, token, 0, 2, moves_played_count)[0]

    def minicycle(self, board, token, last_move, *args):
        return self.m_cycle(board, token, 0, 2, last_move)[0]

    def m_search(self, board, token, depth, max_depth, moves_played_count):
        possible_moves = self.mf.find_moves(board)
        best_move = ''
        best_score = -7000000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            if self.baz.analyze(b, token) > 400000:
                return m, 5000000
            if (depth + 1 >= max_depth):
                h = self.baz.analyze(b, token)
                if h > best_score:
                    best_score = h
                    best_move = m
            else:
                if (moves_played_count >= 23):
                    their_best, h = self.m_cycle(b, self.flipside(token),
                                                 depth+1, max_depth, m)
                else:
                    their_best, h = self.m_search(b, self.flipside(token),
                                                  depth+1, max_depth,
                                                  moves_played_count+1)
                if h*-1 > best_score:
                    best_score = h*-1
                    best_move = m
                    if h == -5000000:
                       break
        return best_move, best_score

    def m_cycle(self, board, token, depth, max_depth, last_move):
        possible_moves = self.mf.find_recyclable(board, last_move)
        best_move = ''
        best_score = -7000000
        for m in possible_moves:
            b = self.bs.copy(board)
            if not self.bs.recycle(b, m, last_move):
                continue
            if self.baz.analyze(b, token) > 400000:
                return m, 5000000
            if (depth + 1 >= max_depth):
                h = self.baz.analyze(b, token)
                if h > best_score:
                    best_score = h
                    best_move = m
            else:
                their_best, h = self.m_cycle(b, self.flipside(token),
                                             depth+1, max_depth, m)
                if h*-1 > best_score:
                    best_score = h*-1
                    best_move = m
                    if h == -5000000:
                       break
        return best_move, best_score


    def naive_single_layer(self, board, token, *args):
        possible_moves = self.mf.find_moves(board)
        best_move = ''
        best_score = -5000000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            h = self.baz.analyze(b, token)
            if h > best_score:
                best_move = m
                best_score = h
        return best_move

    def naive_single_layer_recycle(self, board, token, last_move, *args):
        possible_moves = self.mf.find_recyclable(board, last_move)
        best_move = ''
        best_score = -5000000
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.recycle(b, m, last_move)
            h = self.baz.analyze(b, token)
            if h > best_score:
                best_move = m
                best_score = h
        return best_move

    def chaos_monkey(self, board, token, *args):
        moves = self.mf.find_moves(board)
        shuffle(moves)
        return moves[0]

    def chaos_monkey_recycle(self, board, token, last_move, *args):
        moves = self.mf.find_recyclable(board, last_move)
        shuffle(moves)
        return moves[0]

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"
    
    def chaos(self, func, recycle=False):
        def func_wrapper(board, *args):
            if all(not c[0] for c in board) or random() * 100 < 33:
                print("CHAOS PLAYS")
                if not recycle:
                    return self.chaos_monkey(board, *args)
                return self.chaos_monkey_recycle(board, *args)
            print(func.__name__, "plays")
            return func(board, *args)
        return func_wrapper

