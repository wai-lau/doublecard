from electronic_soul import ElectronicSoul

DEFAULT_OUTPUT_FILE = 'tracemm.txt'
class UselessSoul(ElectronicSoul):
    def __init__(self, bs, baz, mf, generate_trace, sanity=100):
        super().__init__(bs, baz, mf, sanity)
        self.max_depth_heuristic_count = 0
        self.level_2_node_values = []
        self.generate_trace = generate_trace
        if generate_trace:
            self.create_file(DEFAULT_OUTPUT_FILE)

    def move(self, board, token, moves_played_count, *args):
        if self.generate_trace:
            best_move, best_score = self.m_search(board, token, 0, 2, moves_played_count)
            self.append_to_file(DEFAULT_OUTPUT_FILE, str(self.max_depth_heuristic_count))
            self.append_to_file(DEFAULT_OUTPUT_FILE, str(best_score))
            if self.level_2_node_values:
                self.append_to_file(DEFAULT_OUTPUT_FILE, "")
                for node_value in self.level_2_node_values:
                    self.append_to_file(DEFAULT_OUTPUT_FILE, node_value)
                self.append_to_file(DEFAULT_OUTPUT_FILE, "")
            # Clear the list of node-level 2 values for the next search 
            self.level_2_node_values.clear()
            return best_move
        return self.m_search(board, token, 0, 2, moves_played_count)[0]

    def recycle(self, board, token, last_move, *args):
        if self.generate_trace:
            best_move, best_score = self.m_cycle(board, token, 0, 2, last_move)
            self.append_to_file(DEFAULT_OUTPUT_FILE, '\n' + str(best_score))
            return best_move
        return self.m_cycle(board, token, 0, 2, last_move)[0]

    def m_search(self, board, token, depth, max_depth, moves_played_count):
        possible_moves = self.mf.find_moves(board)
        best_move = ''
        best_score = -7000000
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
                # Counting the number of times e(n) has been applied to max depth node
                self.max_depth_heuristic_count += 1
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

                # Filling up the list of e(n) values coming up from level 2
                if max_depth == 2:
                    self.level_2_node_values.append(str(best_score))
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
                self.max_depth_heuristic_count += 1
            else:
                their_best, h = self.m_cycle(b, self.flipside(token),
                                             depth+1, max_depth, m)
                if h*-1 > best_score:
                    best_score = h*-1
                    best_move = m
        return best_move, best_score

    def flipside(self, token):
        return "dots" if token == "colors" else "colors"

    def create_file(self, filename):
        open(filename,'w').close()

    def append_to_file(self, filename, data):
        file = None
        try:
            file = open(filename,'a')
        except:
            # if the file doesn't exist, create it
            file = open(filename,'w')
        file.write(str(data) + '\n')