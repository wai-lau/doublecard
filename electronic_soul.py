from move_finder import MoveFinder

class ElectronicSoul:
    def __init__(self, bs, baz, token='dots'):
        self.mf = MoveFinder()
        self.bs = bs
        self.baz = baz
        self.token = 'dots'

    def get_move(self, board):
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

