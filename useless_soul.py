from electronic_soul import ElectronicSoul

class UselessSoul(ElectronicSoul):
    def move(self, board, token, moves_played_count, *args):
        return self.m_search(board, token, 0, 2, moves_played_count)[0]

    def recycle(self, board, token, last_move, *args):
        return self.m_cycle(board, token, 0, 2, last_move)[0]

    def m_search(self, board, token, depth, max_depth, moves_played_count):
        possible_moves = self.mf.find_moves(board)
        best_move = ''
        best_score = -7000000
        third_node_count = 0
        for m in possible_moves:
            b = self.bs.copy(board)
            self.bs.apply(b, m)
            if (depth + 1 >= max_depth):
                h = self.baz.analyze(b, token)
                if token == "dots":
                    h = h*-1
                if h > best_score:
                    best_score = h
                    best_move = m
                self.count_in_file('output.txt')
                #print('the depth is ' + str(depth))
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
        if depth == 2:
           self.append_to_file('output.txt', str(best_score) + '\n')
        return best_move, best_score

    def m_cycle(self, board, token, depth, max_depth, last_move):
        possible_moves = self.mf.find_recyclable(board, last_move)
        best_move = ''
        best_score = -7000000
        for m in possible_moves:
            b = self.bs.copy(board)
            if not self.bs.recycle(b, m, last_move):
                continue
            if (depth + 1 >= max_depth):
                h = self.baz.analyze(b, token)
                if token == "dots":
                    h = h*-1
                if h > best_score:
                    best_score = h
                    best_move = m
            else:
                their_best, h = self.m_cycle(b, self.flipside(token),
                                             depth+1, max_depth, m)
                if h*-1 > best_score:
                    best_score = h*-1
                    best_move = m
        return best_move, best_score

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"

    def append_to_file(self, filename, data):
        file = None
        try:
            file = open(filename,'a')
        except:
            # if the file doesn't exist, create it
            file = open(filename,'w')
        file.write(data)

    def count_in_file(self, filename):
        with open(filename,'r+') as f:
            value = f.readline().strip() or 0
            f.seek(0)
            f.write(str(int(value) + 1))