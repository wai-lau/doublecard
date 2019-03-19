from electronic_soul import ElectronicSoul

class AlphaLiteSoul(ElectronicSoul):
    def __init__(self, bs, baz, mf, depth=2, hotness=0, sensei=True, **kwargs):
        super().__init__(bs, baz, mf, **kwargs)
        self.depth = depth
        self.hotness = hotness
        self.clear_hot_moves()
        self.moves_played = 0
        self.sensei = sensei

    def clear_hot_moves(self):
        self.hot_moves = [[] for _ in range(self.depth+1)]
        self.new_hot_moves = [[] for _ in range(self.depth+1)]
        self.hot_cycles = [[] for _ in range(self.depth)]
        self.new_hot_cycles = [[] for _ in range(self.depth)]

    def move(self, board, token, moves_played_count, last_move, *args):
        if moves_played_count < self.moves_played:
            self.clear_hot_moves()
        self.moves_played = moves_played_count
        if self.moves_played < 3:
            if self.sensei:
                if not last_move:
                    return self.consult_sensei(token)
                return self.consult_sensei(token, last_move)

        return self.m_search(board, token, 0, self.depth,
                             moves_played_count, -7000000, 7000000)

    def recycle(self, board, token, last_move, *args):
        return self.m_cycle(board, token, 0, self.depth-1,
                            last_move, -7000000, 7000000)

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
        if self.hotness == 0:
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
                if (moves_played_count >= 23):
                    h = self.m_search(b, token, depth+1, depth+1, m, alpha, beta)
                else:
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

    def m_cycle(self, board, token, depth, max_depth,
                 last_move, alpha, beta):
        if depth == max_depth:
            if max_depth%2 == 1:
                return self.baz.analyze(board, token)
            return -1*self.baz.analyze(board, self.flipside(token))
        elif depth%2 == 0:
            value = -7000000
            move = None
            for m in self.mf.find_recyclable(board, last_move):
                b = self.bs.copy(board)
                self.bs.recycle(b, m, last_move)
                if depth < max_depth - 1:
                    h = self.baz.analyze(b, token)
                    if h > 400000:
                        value = h
                        move = m
                        break
                # if depth == 0:
                #     print("Level 0 is trying:", m)
                h = self.m_cycle(b, token, depth+1, max_depth, m, alpha, beta)
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
            for m in self.mf.find_recyclable(board, last_move):
                b = self.bs.copy(board)
                self.bs.recycle(b, m, last_move)
                if depth < max_depth - 1:
                    h = self.baz.analyze(b, self.flipside(token))
                    if h > 400000:
                        value = -1*h
                        move = m
                        break
                h = self.m_cycle(b, token, depth+1, max_depth, m, alpha, beta)
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

    def consult_sensei(self, token, last_move=None):
        token = 0 if token == "dots" else 1
        knowledge = {
            "NONE": [ [1, 'C', 1] , [1, 'C', 1] ],
            "2A1": [ [5, 'D', 1] , [7, 'D', 1] ],
            "4A1": [ [7, 'D', 1] , [5, 'D', 1] ],
            "6A1": [ [1, 'D', 1] , [3, 'D', 1] ],
            "8A1": [ [3, 'D', 1] , [1, 'D', 1] ],
            "2B1": [ [6, 'F', 1] , [8, 'F', 1] ],
            "4B1": [ [8, 'F', 1] , [6, 'F', 1] ],
            "6B1": [ [2, 'F', 1] , [4, 'F', 1] ],
            "8B1": [ [4, 'F', 1] , [2, 'F', 1] ],
            "2C1": [ [8, 'D', 1] , [6, 'D', 1] ],
            "4C1": [ [6, 'D', 1] , [8, 'D', 1] ],
            "6C1": [ [4, 'D', 1] , [2, 'D', 1] ],
            "8C1": [ [2, 'D', 1] , [4, 'D', 1] ],
            "2D1": [ [8, 'C', 1] , [6, 'C', 1] ],
            "4D1": [ [6, 'C', 1] , [8, 'C', 1] ],
            "6D1": [ [4, 'C', 1] , [2, 'C', 1] ],
            "8D1": [ [2, 'C', 1] , [4, 'C', 1] ],
            "2E1": [ [8, 'F', 1] , [6, 'F', 1] ],
            "4E1": [ [6, 'F', 1] , [8, 'F', 1] ],
            "6E1": [ [4, 'F', 1] , [2, 'F', 1] ],
            "8E1": [ [2, 'F', 1] , [4, 'F', 1] ],
            "2F1": [ [8, 'E', 1] , [6, 'E', 1] ],
            "4F1": [ [6, 'E', 1] , [8, 'E', 1] ],
            "6F1": [ [4, 'E', 1] , [2, 'E', 1] ],
            "8F1": [ [2, 'E', 1] , [4, 'E', 1] ],
            "2G1": [ [6, 'C', 1] , [8, 'C', 1] ],
            "4G1": [ [8, 'C', 1] , [6, 'C', 1] ],
            "6G1": [ [2, 'C', 1] , [4, 'C', 1] ],
            "8G1": [ [4, 'C', 1] , [2, 'C', 1] ],
            "2H1": [ [7, 'D', 1] , [5, 'D', 1] ],
            "4H1": [ [5, 'D', 1] , [7, 'D', 1] ],
            "6H1": [ [3, 'D', 1] , [1, 'D', 1] ],
            "8H1": [ [1, 'D', 1] , [3, 'D', 1] ],
            "1A1": [ [5, 'E', 1] , [7, 'E', 1] ],
            "3A1": [ [7, 'E', 1] , [5, 'E', 1] ],
            "5A1": [ [1, 'E', 1] , [3, 'E', 1] ],
            "7A1": [ [3, 'E', 1] , [1, 'E', 1] ],
            "1B1": [ [7, 'B', 2] , [5, 'B', 2] ],
            "3B1": [ [5, 'B', 2] , [7, 'B', 2] ],
            "5B1": [ [3, 'B', 2] , [1, 'B', 2] ],
            "7B1": [ [1, 'B', 2] , [3, 'B', 2] ],
            "1C1": [ [7, 'C', 2] , [5, 'C', 2] ],
            "3C1": [ [5, 'C', 2] , [7, 'C', 2] ],
            "5C1": [ [3, 'C', 2] , [1, 'C', 2] ],
            "7C1": [ [1, 'C', 2] , [3, 'C', 2] ],
            "1D1": [ [6, 'A', 1] , [8, 'A', 1] ],
            "3D1": [ [8, 'A', 1] , [6, 'A', 1] ],
            "5D1": [ [2, 'A', 1] , [4, 'A', 1] ],
            "7D1": [ [4, 'A', 1] , [2, 'A', 1] ],
            "1E1": [ [7, 'E', 2] , [5, 'E', 2] ],
            "3E1": [ [5, 'E', 2] , [7, 'E', 2] ],
            "5E1": [ [3, 'E', 2] , [1, 'E', 2] ],
            "7E1": [ [1, 'E', 2] , [3, 'E', 2] ],
            "1F1": [ [7, 'F', 2] , [5, 'F', 2] ],
            "3F1": [ [5, 'F', 2] , [7, 'F', 2] ],
            "5F1": [ [3, 'F', 2] , [1, 'F', 2] ],
            "7F1": [ [1, 'F', 2] , [3, 'F', 2] ],
            "1G1": [ [5, 'C', 1] , [7, 'C', 1] ],
            "3G1": [ [7, 'C', 1] , [5, 'C', 1] ],
            "5G1": [ [1, 'C', 1] , [3, 'C', 1] ],
            "7G1": [ [3, 'C', 1] , [1, 'C', 1] ]
        }
        defensive_knowledge = {
            "2A1": [ [6, 'C', 2] , [8, 'C', 2] ],
            "4A1": [ [8, 'C', 2] , [6, 'C', 2] ],
            "6A1": [ [2, 'C', 2] , [4, 'C', 2] ],
            "8A1": [ [4, 'C', 2] , [2, 'C', 2] ],
            "2B1": [ [6, 'D', 2] , [8, 'D', 2] ],
            "4B1": [ [8, 'D', 2] , [6, 'D', 2] ],
            "6B1": [ [2, 'D', 2] , [4, 'D', 2] ],
            "8B1": [ [4, 'D', 2] , [2, 'D', 2] ],
            "2C2": [ [8, 'D', 2] , [6, 'D', 2] ],
            "4C2": [ [6, 'D', 2] , [8, 'D', 2] ],
            "6C2": [ [4, 'D', 2] , [4, 'E', 1] ],
            "8C2": [ [4, 'E', 1] , [4, 'D', 2] ],
            "2D2": [ [6, 'B', 1] , [8, 'B', 1] ],
            "4D2": [ [8, 'F', 1] , [6, 'F', 1] ],
            "6D2": [ [2, 'B', 1] , [4, 'B', 1] ],
            "8D2": [ [4, 'B', 1] , [2, 'B', 1] ],
            "2E1": [ [8, 'G', 1] , [6, 'G', 1] ],
            "4E1": [ [8, 'C', 2] , [6, 'C', 2] ],
            "6E1": [ [4, 'G', 1] , [4, 'C', 2] ],
            "8E1": [ [4, 'C', 2] , [4, 'G', 1] ],
            "2F1": [ [8, 'F', 3] , [6, 'F', 3] ],
            "4F1": [ [6, 'E', 1] , [8, 'E', 1] ],
            "6F1": [ [4, 'E', 1] , [4, 'D', 2] ],
            "8F1": [ [4, 'D', 2] , [4, 'E', 1] ],
            "2G1": [ [6, 'G', 3] , [8, 'G', 3] ],
            "4G1": [ [6, 'E', 1] , [8, 'E', 1] ],
            "6G1": [ [4, 'E', 1] , [8, 'G', 3] ],
            "8G1": [ [6, 'G', 3] , [4, 'E', 1] ],
            "2H1": [ [8, 'G', 1] , [6, 'G', 1] ],
            "4H1": [ [3, 'C', 2] , [3, 'C', 2] ],
            "6H1": [ [8, 'G', 1] , [5, 'C', 2] ],
            "8H1": [ [7, 'C', 2] , [6, 'G', 1] ],
            "1A1": [ [8, 'C', 2] , [6, 'C', 2] ],
            "3A1": [ [1, 'F', 1] , [1, 'F', 1] ],
            "5A1": [ [4, 'C', 2] , [4, 'B', 2] ],
            "7A1": [ [4, 'B', 2] , [4, 'C', 2] ],
            "1C2": [ [7, 'C', 3] , [5, 'C', 3] ],
            "3C2": [ [6, 'H', 1] , [8, 'H', 1] ],
            "5C2": [ [2, 'C', 3] , [5, 'C', 3] ],
            "7C2": [ [7, 'C', 3] , [2, 'C', 3] ],
            "1E1": [ [6, 'D', 2] , [8, 'D', 2] ],
            "3E1": [ [7, 'A', 1] , [5, 'A', 1] ],
            "5E1": [ [2, 'D', 2] , [3, 'A', 1] ],
            "7E1": [ [3, 'A', 1] , [2, 'D', 2] ],
            "1F1": [ [3, 'A', 1] , [3, 'A', 1] ],
            "3F1": [ [6, 'E', 1] , [8, 'E', 1] ],
            "5F1": [ [3, 'A', 1] , [4, 'A', 1] ],
            "7F1": [ [4, 'A', 1] , [3, 'A', 1] ],
            "1G1": [ [7, 'C', 2] , [5, 'C', 2] ],
            "3G1": [ [7, 'C', 2] , [5, 'C', 2] ],
            "5G1": [ [2, 'G', 2] , [5, 'E', 1] ],
            "7G1": [ [7, 'E', 1] , [2, 'G', 2] ]
        }
        if not last_move:
            return knowledge["NONE"][token]
        if self.moves_played < 2:
            return knowledge["".join(map(str, last_move))
                             .replace("0","").upper()][token]
        return defensive_knowledge["".join(map(str, last_move))
                                   .replace("0","").upper()][token]
