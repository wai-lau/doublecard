from board_analyzer import BoardAnalyzer
import re
# Convention: Dots is position 0, Colors position 1

class ThickAnalyzer(BoardAnalyzer):
    def __init__(self, ach):
        self.ach = ach

    def check_victory(self, board, token):
        heuristic = self.analyze(board, token)
        if heuristic > 400000:
            return token

    def analyze(self, board, token):
        t_board = list(zip(*board))

        if not "".join(t_board[0]):
            return 0

        ft_board = self.fill_board(t_board)
        st_board = self.support_board(t_board)

        cols = [self.convert_line(("".join(col))[-4*2:])
                for col in board if len("".join(col)) >= 2*2]
        rows = [[c + " " + st_board[r] for c \
                in self.convert_line("".join(ft_board[r]))]
                for r, row in enumerate(t_board) if len("".join(row)) >= 2*2]
        dags = self.diagonals(ft_board, st_board) + \
                self.diagonals(self.flip_board(ft_board),
                               self.flip_board(st_board))

        lines = cols + rows + dags
        dots, colors = zip(*lines)
        
        if token == "dots":
            return (sum(self.fetch_line(d, 0) for d in dots) -
                    sum(self.fetch_line(c, 1) for c in colors))
        return (sum(self.fetch_line(c, 0) for c in colors) -
                sum(self.fetch_line(d, 1) for d in dots))

    def fetch_line(self, line, possesion):
        return (self.ach.cache[line][possesion])

    def diagonals(self, ft_board, st_board):
        dags = []
        rows = len(ft_board)
        cols = len(ft_board[0])
        length = 7
        done = False
        for c in range(1, 5):
            d = []
            s = ""
            for i in range(length):
                d.append(ft_board[0+i][c+i])
                s += st_board[0+i][c+i]
            d = "".join(d)
            if len(d.replace("0","")) >= 2*2:
                dags.append([co + " " + s for co in self.convert_line(d)])
            length -= 1

        length = 8
        for r in range(9):
            d = []
            s = ""
            for i in range(length):
                d.append(ft_board[r+i][0+i])
                s += st_board[r+i][0+i]
            d = "".join(d)
            if len(d.replace("0","")) >= 2*2:
                dags.append([c + " " + s for c in self.convert_line(d)])
            else:
                break
            if r >= 4:
                length -= 1
    
        return (dags)

    def flip_board(self, t_board):
        return [r[::-1] for r in t_board]

    def convert_line(self, line):
        col_row = line[::2].replace("W", "1").replace("R", "2")
        dot_row = re.sub(r'[^20]', "1",
                         re.sub(r'[►▼▲◄]',"2", line[1::2]))
        return (dot_row, col_row)

    def fill_board(self, board):
        return [[(e if e else "00") for e in col] for col in board]

    def support_board(self, t_board):
        s_board = []
        for r, row in enumerate(t_board):
            if r <= 1:
                s_board.append("11111111")
            else:
                s_board.append("".join(list(map(
                    lambda x, y: "1" if x or y else "0", t_board[r-1], t_board[r-2]
                ))))
        return s_board
