from electronic_soul import ElectronicSoul

class NaiveSoul(ElectronicSoul):
    def move(self, board, token, moves_played_count, *args):
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

    def recycle(self, board, token, last_move, *args):
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
