import os
from random import shuffle, random

class ElectronicSoul:
    def __init__(self, bs, baz, mf, sanity=100):
        self.mf = mf
        self.bs = bs
        self.baz = baz
        if sanity <= 0:
            self.move = self.chaos_monkey
            self.recycle = self.chaos_monkey_recycle
        # Else children should implement move and recycle
        if sanity < 100:
            self.move = self.chaos(self.move, sanity=sanity)
            self.recycle = self.chaos(self.recycle, recycle=True, sanity=sanity)

    # for recursive searching, we need to be careful on the transition
    # from regular move to recycling moves
    def get_move(self, board, token, last_move=None, moves_played_count=None):
        if moves_played_count and moves_played_count >= 24:
            return self.recycle(board, token, last_move)
        return self.move(board, token, moves_played_count, last_move)

    def move(self, board, token, moves_played_count):
        raise NotImplementedError

    def recycle(self, board, token, last_move):
        raise NotImplementedError

    def chaos_monkey(self, board, token, *args):
        moves = self.mf.find_moves(board)
        shuffle(moves)
        return moves[0]

    def chaos_monkey_recycle(self, board, token, last_move, *args):
        moves = self.mf.find_recyclable(board, last_move)
        shuffle(moves)
        return moves[0]

    def chaos(self, func, recycle=False, sanity=77):
        def func_wrapper(board, *args):
            if all(not c[0] for c in board) or (random() * 100) < (100-sanity):
                if not recycle:
                    return self.chaos_monkey(board, *args)
                return self.chaos_monkey_recycle(board, *args)
            return func(board, *args)
        return func_wrapper

