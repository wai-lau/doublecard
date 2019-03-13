from electronic_soul import ElectronicSoul

class AlphaLiteSoul(ElectronicSoul):
    def __init__(self, bs, baz, mf, depth=2, hotness=0, **kwargs):
        super().__init__(bs, baz, mf, **kwargs)
        self.depth = depth
        self.hotness = hotness
        self.clear_hot_moves()
        self.moves_played = 0

    def clear_hot_moves(self):
        self.hot_moves = [[] for _ in range(self.depth+1)]
        self.new_hot_moves = [[] for _ in range(self.depth+1)]
        self.hot_cycles = [[] for _ in range(self.depth)]
        self.new_hot_cycles = [[] for _ in range(self.depth)]

    def move(self, board, token, moves_played_count, *args):
        if moves_played_count < self.moves_played:
            self.clear_hot_moves()
        self.moves_played = moves_played_count

        return self.m_search(board, token, 0, self.depth, moves_played_count, 7000000)

    def recycle(self, board, token, last_move, *args):
        return self.m_cycle(board, token, 0, self.depth-1, last_move, 7000000)

    def find_hot_moves(self, board, depth):
        possible_moves = self.mf.find_moves(board)
        for m in self.hot_moves[depth]:
            if m in possible_moves:
                possible_moves.remove(m)
                possible_moves.append(m)
        return possible_moves

    def update_hot_moves(self):
        for d, moves in enumerate(self.new_hot_moves):
            del moves[:-self.hotness]
            for m in moves:
                if m[1] not in self.hot_moves[d]:
                    self.hot_moves[d].append(m[1])
            del self.hot_moves[d][:-2*self.hotness]
            del moves[:]

    def possible_moves(self, board, depth, moves_played_count=4):
        if self.hotness == 0 or moves_played_count <= 3:
            return self.mf.find_moves(board)
        else:
            if (0 == depth):
                self.update_hot_moves()
            return list(reversed(self.find_hot_moves(board, depth)))

    # notation here describes who the heuristic is best for
    # and that position analyzed which perspective
    def m_search(self, board, token, depth, max_depth,
                 moves_played_count, best):
        # these initial values are meant to be overwritten so don't worry to much about them
        # but you need to set them big enough and the right sign
        best_score = -7000000
        hot_move = None

        possible_moves = self.possible_moves(board, depth, moves_played_count)
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            h = self.baz.analyze(b, token)

            if h > 400000:
                hot_move = m
                if depth == 0:
                    return m
                return 5000000

            if depth >= max_depth:
                if h > best_score:
                    hot_move = m
                    best_score = h

            else:
                h = -1*self.m_search(b, self.flipside(token), depth+1, max_depth,
                                     moves_played_count,
                                     best=-1*best_score)
                if h > best_score:
                    hot_move = m
                    best_score = h
        
            # this is the pruning, if your adversary knows how to get to a weaker set of moves
            # then they will force you to go over there anyway, no need to analyze this further
            if best_score >= best:
                hot_move = None
                break

        if self.hotness != 0 and hot_move:
            self.add_hot_move(depth, best_score, hot_move)

        if depth == 0:
            return hot_move
        return best_score

    def add_hot_move(self, depth, best_score, hot_move):
        if not self.new_hot_moves[depth]:
            self.new_hot_moves[depth].append((best_score, hot_move))
        elif best_score > self.new_hot_moves[depth][-1][0]:
            self.new_hot_moves[depth].append((best_score, hot_move))

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"

