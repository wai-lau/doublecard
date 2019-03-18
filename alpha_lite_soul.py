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

        return self.m_search(board, token, 0, self.depth,
                             moves_played_count, -7000000, 7000000)

    def recycle(self, board, token, last_move, *args):
        return self.m_cycle(board, token, 0, self.depth-1,
                            last_move, 7000000)

    def find_hot_moves(self, board, depth):
        possible_moves = self.mf.find_moves(board)
        if self.hotness <= 0:
            return possible_moves
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
            # reversing list so that we just append and recreate the list once
            # instead of constantly shifting the entire list
            return list(reversed(self.find_hot_moves(board, depth)))

    def m_search(self, board, token, depth, max_depth,
                 moves_played_count, alpha, beta):
        if depth == max_depth:
            if max_depth%2 == 1:
                return self.baz.analyze(board, token)
            return -1*self.baz.analyze(board, self.flipside(token))
        elif depth%2 == 0:
            value = -7000000
            move = None
            for m in self.find_hot_moves(board, depth):
                b = self.bs.copy(board)
                self.bs.apply(b, m)
                if depth < max_depth - 1:
                    h = self.baz.analyze(b, token)
                    if h > 400000:
                        value = h
                        move = m
                        break
                # if depth == 0:
                #     print("Level 0 is trying:", m)
                h = self.m_search(b, token, depth+1, max_depth, moves_played_count, alpha, beta)
                if h > value:
                    value = h
                    move = m
                alpha = max(alpha, value)
                if alpha >= beta:
                   break
            self.add_hot_move(depth, value, move)
            if depth == 0:
                # print("Ultimately they played:", move, value)
                return move
            return value
        elif depth%2 == 1:
            value = 7000000
            move = None
            for m in self.find_hot_moves(board, depth):
                b = self.bs.copy(board)
                self.bs.apply(b, m)
                if depth < max_depth - 1:
                    h = self.baz.analyze(b, self.flipside(token))
                    if h > 400000:
                        value = -1*h
                        move = m
                        break
                h = self.m_search(b, token, depth+1, max_depth, moves_played_count, alpha, beta)
                if h < value:
                    value = h
                    move = m
                beta = min(beta, value)
                if alpha >= beta:
                    break
            # print(depth*"  ","Expecting response: ", move, value)
            self.add_hot_move(depth, value, move)
            return value

    def add_hot_move(self, depth, best_score, hot_move):
        if not self.new_hot_moves[depth]:
            self.new_hot_moves[depth].append((best_score, hot_move))
        elif depth%2 == 0:
            if best_score > self.new_hot_moves[depth][-1][0]:
                self.new_hot_moves[depth].append((best_score, hot_move))
        else:
            if best_score < self.new_hot_moves[depth][-1][0]:
                self.new_hot_moves[depth].append((best_score, hot_move))

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"

