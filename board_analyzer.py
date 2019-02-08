from functools import reduce
# Convention: Dots is position 0, Colors position 1

class BoardAnalyzer:
    def __init__(self, ach=None):
        self.ach = ach

    def check_victory(self, board):
        # doesn't matter which side the analysis is done on for victory
        # but it's probably good to throw an error when people don't
        # specify a side, sooooo
        dots, colors = self.analyze(board, "dots", verbose=False)
        if dots[4] and colors[4]:
            return "active"
        elif dots[4]:
            return "dots"
        elif colors[4]:
            return "colors"

    def analyze(self, board, token, verbose=False):
        t_board = list(zip(*board))

        if not "".join(t_board[0]):
            return (0,0,0,0,0), (0,0,0,0,0)

        cols = [col for col in board if "".join(col)]
        rows = [row for row in t_board if "".join(row)]
        dags = [dag for dag in self.diagonals(board)
                + self.diagonals(self.flip_board(board))
                if "".join(dag)]

        lines = cols + rows + dags

        points = list(zip(*map(self.fetch_line, lines)))
        dot_points = list(map(sum, list(zip(*points[0]))))
        color_points = list(map(sum, list(zip(*points[1]))))

        if verbose:
            self.print_analysis((dot_points, color_points))

        return dot_points, color_points

    def heuristic(self, board, token, verbose=False):
        d, c = self.analyze(board, token, verbose)
        pot = 0
        if token == "dots":
            pot = self.potential(d) - self.enemy_potential(c)
        else:
            pot = self.potential(c) - self.enemy_potential(d)
        if verbose:
            print(pot)
        return pot

    def potential(self, points):
        pot = 0
        # since we take a subset, points[0] is the number of doubles
        # using a multiple of 100 if it outclasses in all cases
        for i, n in enumerate(points[2:]):
            pot = pot + {0:2, 1:7, 2:1000000000}[i]*n
        return pot

    def enemy_potential(self, points):
        pot = 0
        # enemy triples are worth as much as a loss, since they will play that move 
        for i, n in enumerate(points[2:]):
            pot = pot + {0:7, 1:10000, 2:1000000}[i]*n
        return pot

    def print_analysis(self, analysis):
        dot_points = analysis[0]
        color_points = analysis[1]
        for i in range(1,5):
            print("D: {} potential 4-in-a-row group with {} filled."
                  .format(dot_points[i], i))
            print("C: {} potential 4-in-a-row group with {} filled."
                  .format(color_points[i], i))

    def fetch_line(self, line):
        line = self.convert_line(line)
        return (self.ach.cache[line[0]],
                self.ach.cache[line[1]])

    def diagonals(self, board, diag=4):
        # This algo assumes there are more rows than columns
        # |XX
        # |XX
        # |--
        # |
        # once you reach the square, you must start reducing the diagonal length

        dags = []
        cols = len(board)
        rows = len(board[0])
        length = cols
        for r in range(rows - diag + 1):
            if (r+cols > rows):
                length = length-1
            d = []
            for i in range(length):
                d.append(board[0+i][r+i])
            dags.append(d)

        length = cols-1
        for c in range(1, cols - diag + 1):
            d = []
            for i in range(length):
                d.append(board[c+i][0+i])
            dags.append(d)
            length = length-1

        return(dags)

    def flip_board(self, board):
        return [c for c in reversed(board)]

    def convert_line(self, line):
        dot = ""
        color = ""
        for c in line:
            if not c:
                dot = dot + "0"
                color = color + "0"
                continue
            if c[1] in ['▶','▲','▼','◀']:
                dot = dot + "1"
            else:
                dot = dot + "2"
            if c[0] == "R":
                color = color + "1"
            else:
                color = color + "2"
        return (dot, color)

