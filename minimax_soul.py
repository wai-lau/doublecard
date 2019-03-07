from electronic_soul import ElectronicSoul

class MinimaxSoul(ElectronicSoul):
    def move(self, board, token, moves_played_count, *args):
        return self.m_search(board, token, 0, 2, moves_played_count)[0]

    def recycle(self, board, token, last_move, *args):
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

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"

