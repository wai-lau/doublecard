from functools import reduce
# Convention: Dots is position 0, Colors position 1

class BoardAnalyzer:
    def __init__(self, ach=None):
        self.ach = ach

    def check_victory(self, board, token):
        heuristic = self.analyze(board, token)
        if heuristic > 400000:
            return token

    def analyze(self, board, token):
        t_board = list(zip(*board))

        if not "".join(t_board[0]):
            return (0,0,0,0,0), (0,0,0,0,0)

        cols = [col for col in board if "".join(col)]
        rows = [row for row in t_board if "".join(row)]
        dags = [dag for dag in self.diagonals(board)
                + self.diagonals(self.flip_board(board))
                if "".join(dag)]

        lines = cols + rows + dags

        lines = map(self.convert_line, lines)
        dots, colors = zip(*lines)
        if token == "dots":
            return (sum(self.fetch_line(d, 0) for d in dots) -
                    sum(self.fetch_line(c, 1) for c in colors))
        return (sum(self.fetch_line(c, 0) for c in colors) -
                sum(self.fetch_line(d, 1) for d in dots))

    def fetch_line(self, line, possesion):
        return (self.ach.cache[line][possesion])

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
            if c[1] in ['►','▲','▼','◄']:
                dot = dot + "1"
            else:
                dot = dot + "2"
            if c[0] == "R":
                color = color + "1"
            else:
                color = color + "2"
        return (dot, color)
