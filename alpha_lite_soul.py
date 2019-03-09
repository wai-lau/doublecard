from electronic_soul import ElectronicSoul

class AlphaLiteSoul(ElectronicSoul):
    def __init__(self, bs, baz, mf, depth=2, **kwargs):
        super().__init__(bs, baz, mf, **kwargs)
        self.depth = depth
        self.hot_moves = {0:[], 1:[]}
        self.hot_cycles = {0:[], 1:[]}

    def move(self, board, token, moves_played_count, *args):
        return self.m_search(board, token, 0, self.depth, moves_played_count, 7000000)

    def recycle(self, board, token, last_move, *args):
        return self.m_cycle(board, token, 0, self.depth-1, last_move, 7000000)

    def find_hot_moves(self, board, depth):
        possible_moves = self.mf.find_moves(board)
        del self.hot_moves[depth][:-20]
        for m in self.hot_moves[depth]:
            if m in possible_moves:
                possible_moves.remove(m)
                possible_moves.append(m)
        return possible_moves

    # notation here describes who the heuristic is best for
    # and that position analyzed which perspective
    def m_search(self, board, token,
                 depth, max_depth,
                 moves_played_count,
                 best):
        possible_moves = list(reversed(self.find_hot_moves(board, depth%2)))
        if (0 == depth):
            our_best_our_perspective = -7000000
            best_move = possible_moves[0]
            for m in possible_moves:
                b = self.bs.copy(board)
                self.bs.apply(b, m)

                # if you can win, play that move
                if self.baz.analyze(b, token) > 400000:
                    return m

                # assume your adversary will make the best move
                th = -1*self.m_search(b, self.flipside(token), depth+1, max_depth,
                                      moves_played_count,
                                      best=-1*our_best_our_perspective)

                # make the move that reduces his damage the most
                if th > our_best_our_perspective:
                    our_best_our_perspective = th
                    best_move = m
            return best_move
    
        if (0 < depth < max_depth):
            # these initial values are meant to be overwritten so don't worry to much about them
            # but you need to set them big enough and the right sign
            our_worst_our_perspective = 7000000
            our_best_our_perspective = -7000000
            for m in possible_moves:
                b = self.bs.copy(board)
                self.bs.apply(b, m)

                h = self.baz.analyze(b, token)
                if h > 400000:
                    return 5000000

                th = -1*self.m_search(b, self.flipside(token), depth+1, max_depth,
                                      moves_played_count,
                                      best=-1*our_best_our_perspective)
                
                # we pick the move that minimizes damage
                # and we pass up that analysis our perspective
                if th > our_best_our_perspective:
                    our_best_our_perspective = th

                # killer heuristic
                if th < our_worst_our_perspective:
                    our_worst_their_perspective = th
                    hot_move = m

                # this is the pruning, if your adversary knows how to get to a weaker set of moves
                # then they will force you to go over there anyway, no need to analyze this further
                if our_best_our_perspective >= best:
                    break
            if not hot_move in self.hot_moves[(depth % 2)]:
                self.hot_moves[(depth % 2)].append(hot_move)
            return our_best_our_perspective

        else:
            our_worst_our_perspective = 7000000
            our_best_our_perspective = -7000000
            for m in possible_moves:
                b = self.bs.copy(board)
                self.bs.apply(b, m)
                
                h = self.baz.analyze(b, token)
                if h > 400000:
                    return 5000000

                if h > our_best_our_perspective:
                    our_best_our_perspective = h
                
                # killer heuristic
                if h < our_worst_our_perspective:
                    our_worst_our_perspective = h
                    hot_move = m
                
                if our_best_our_perspective >= best:
                    break
            if not hot_move in self.hot_moves[(depth % 2)]:
                self.hot_moves[(depth % 2)].append(hot_move)
            return our_best_our_perspective

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"

