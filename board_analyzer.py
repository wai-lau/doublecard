from functools import reduce

class BoardAnalyzer:
    def analyze(self, board):
        col_points = list(zip(*[self.check_line(col) for col in board if "".join(col)]))
        if len(col_points) <= 0:
            print("No moves played.")
            return
        t_board = zip(*board)
        row_points = list(zip(*[self.check_line(r) for r in t_board if "".join(r)]))

        add = lambda x, y: x+y

        # looks ugly
        dot_col_points = list(zip(*col_points[0]))
        dot_row_points = list(zip(*row_points[0]))
        color_col_points = list(zip(*col_points[1]))
        color_row_points = list(zip(*row_points[1]))

        for i in range(1,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("DOT", reduce(add, dot_col_points[i]), "column", i))
        for i in range(1,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("DOT", reduce(add, dot_row_points[i]), "row", i))
        for i in range(1,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("COLOR", reduce(add, color_col_points[i]), "column", i))
        for i in range(1,5):
            print("{}: {} potential 4 in a {} group with {} filled."
                    .format("COLOR", reduce(add, color_row_points[i]), "row", i))


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

            if len(dot_group) == 0:
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
