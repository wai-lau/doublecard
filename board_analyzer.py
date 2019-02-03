from functools import reduce
# Convention: Dots is position 0, Colors position 1

class BoardAnalyzer:
    def __init__(self, ach=None):
        self.ach = ach

    def analyze(self, board):
        t_board = list(zip(*board))

        if not "".join(t_board[0]):
            print("No moves played")
            return

        cols = [col for col in board if "".join(col)]
        rows = [row for row in t_board if "".join(row)]
        dags = [dag for dag in self.diagonals(board)
                + self.diagonals(self.flip_board(board))
                if "".join(dag)]

        lines = cols + rows + dags

        if self.ach:
            checker = self.fetch_line
        else:
            checker = self.check_line

        points = list(zip(*map(checker, lines)))
        dot_points = list(map(sum, list(zip(*points[0]))))
        color_points = list(map(sum, list(zip(*points[1]))))

        for i in range(1,5):
            print("D: {} potential 4-in-a-row group with {} filled."
                  .format(dot_points[i], i))
            print("C: {} potential 4-in-a-row group with {} filled."
                  .format(color_points[i], i))

        if dot_points[4] and color_points[4]:
            return "active"
        elif dot_points[4]:
            return "dots"
        elif color_points[4]:
            return "colors"

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
        # |
        # |
        # |
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

    def check_line(self, line):
        # the number of groups of 4 in a line will be the length-3
        groups = len(line)-3

        # dot[2] will give you the number of unblocked doubles
        # dot[3] triples etc...
        dot = [0,0,0,0,0]
        color = [0,0,0,0,0]

        if groups <= 0:
            return (dot, color)

        for s in range(groups):
            # a possible optimization here could be to stop searching
            # once you find a four in a row
            dot_group = [l[1] for l in line[s:s+4] if l]

            if not "".join(dot_group):
                # this means this group is empty
                continue
            color_group = [l[0] for l in line[s:s+4] if l]

            if (not any(sym in dot_group for sym in ['▶','▲','▼','◀']))\
            or (not any(sym in dot_group for sym in ['▷','△','▽','◁'])):
                dot[len(dot_group)] = dot[len(dot_group)]+1

            if (not 'R' in color_group)\
            or (not 'W' in color_group):
                color[len(color_group)] = color[len(color_group)]+1

        return (dot, color)

