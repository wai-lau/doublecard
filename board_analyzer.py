from functools import reduce

class BoardAnalyzer:
    def analyze(self, board):
        col_points = list(zip(*[self.check_line(col) for col in board if "".join(col)]))
        if len(col_points) <= 0:
            print("No moves played.")
            return
        t_board = list(zip(*board))
        row_points = list(zip(*[self.check_line(r) for r in t_board if "".join(r)]))

        add = lambda x, y: x+y

        diag_points = list(zip(*[self.check_line(d) for d in self.diagonals(board)+self.diagonals(self.flip_board(board)) if "".join(d)]))

        # up until the return, this is only used for displaying stuff
        dot_col_points = list(zip(*col_points[0]))
        color_col_points = list(zip(*col_points[1]))
        dot_row_points = list(zip(*row_points[0]))
        color_row_points = list(zip(*row_points[1]))
        dot_diag_points = list(zip(*diag_points[0]))
        color_diag_points = list(zip(*diag_points[1]))

        for i in range(2,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("D", reduce(add, dot_col_points[i]), "column", i))
        for i in range(2,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("D", reduce(add, dot_row_points[i]), "row", i))
        for i in range(2,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("D", reduce(add, dot_diag_points[i]), "diagonal", i))

        print()

        for i in range(2,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("C", reduce(add, color_col_points[i]), "column", i))
        for i in range(2,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("C", reduce(add, color_row_points[i]), "row", i))
        for i in range(2,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("C", reduce(add, color_diag_points[i]), "diagonal", i))

        if (reduce(add, dot_col_points[4]) or
            reduce(add, dot_row_points[4]) or
            reduce(add, dot_diag_points[4])) and\
            (reduce(add, color_col_points[4]) or
            reduce(add, color_row_points[4]) or
            reduce(add, color_diag_points[4])):
            return "active"

        if (reduce(add, dot_col_points[4]) or
            reduce(add, dot_row_points[4]) or
            reduce(add, dot_diag_points[4])):
            return "dots"

        if (reduce(add, color_col_points[4]) or
            reduce(add, color_row_points[4]) or
            reduce(add, color_diag_points[4])):
            return "colors"

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

        diags = []
        cols = len(board)
        rows = len(board[0])
        length = cols
        for r in range(rows - diag + 1):
            if (r+cols > rows):
                length = length-1
            d = []
            for i in range(length):
                d.append(board[0+i][r+i])
            diags.append(d)

        length = cols-1
        for c in range(1, cols - diag + 1):
            d = []
            for i in range(length):
                d.append(board[c+i][0+i])
            diags.append(d)
            length = length-1

        return(diags)

    def flip_board(self, board):
        return [c for c in reversed(board)]
