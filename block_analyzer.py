from board_analyzer import BoardAnalyzer

class BlockAnalyzer(BoardAnalyzer):
    def __init__(self, ach):
        self.ach = ach

    def check_victory(self, board, token):
        heuristic = self.analyze(board, token)
        if heuristic > 400000:
            return token

    def analyze(self, board, token):
        board = self.convert_board(board)
        t_board = list(zip(*board))
        if "00000000" == "".join(t_board[0]):
            return 0

        bboard = self.b_board(board)
        t_bboard = list(zip(*bboard))

        cols = ["".join(col).replace("0","")[-4:] for col in board if len("".join(col).replace("0",""))>=2]
        rows = []
        for r, row in enumerate(t_board):
            for c, _ in enumerate(row[:5]):
                if len("".join(row[c:c+4]).replace("0","")) >= 2:
                    if r <= 1:
                        rows.append("".join(row[c:c+4])+"11111111")
                    else:
                        rows.append("".join(
                            row[c:c+4]+
                            t_bboard[r-1][c:c+4]+
                            t_bboard[r-2][c:c+4]
                        ))
                                
        dags = self.diagonals(board, bboard) + \
               self.diagonals(self.flip_board(board), self.flip_board(bboard))

        possession = 0 if token == "dots" else 1
        return sum([self.fetch_line(l, possession) for l in cols + rows + dags])

    def fetch_line(self, line, possesion):
        return (self.ach.cache[line][possesion])

    def diagonals(self, board, bboard):
        dags = []
        for c, col in enumerate(board[:5]):
            for r, _ in enumerate(col[:9]):
                if len((board[c][r] + board[c+1][r+1] + board[c+2][r+2] + board[c+3][r+3]).replace("0","")) >= 2:
                    if r == 0:
                        dags.append(board[c][r] + board[c+1][r+1] + board[c+2][r+2] + board[c+3][r+3] +
                                    "1" + "1" + bboard[c+2][r+1] + bboard[c+3][r+2] +
                                    "1" + "1" + bboard[c+2][r  ] + bboard[c+3][r+1]
                                   )
                    elif r == 1:
                        dags.append(board[c][r] + board[c+1][r+1] + board[c+2][r+2] + board[c+3][r+3] +
                                    "1" + bboard[c+1][r  ] + bboard[c+2][r+1] + bboard[c+3][r+2] +
                                    "1" + bboard[c+1][r-1] + bboard[c+2][r  ] + bboard[c+3][r+1]
                                   )
                    else:
                        dags.append(board[c][r  ] + board[c+1][r+1] + board[c+2][r+2] + board[c+3][r+3] +
                                    bboard[c][r-1] + bboard[c+1][r  ] + bboard[c+2][r+1] + bboard[c+3][r+2] +
                                    bboard[c][r-2] + bboard[c+1][r-1] + bboard[c+2][r  ] + bboard[c+3][r+1]
                                   )

        return(dags)

    def flip_board(self, board):
        return [c for c in reversed(board)]

    def convert_board(self, board):
        return [[self.convert_sym(e) for e in col] for col in board]
                
    def convert_sym(self, sym):
        return {
            "":"0",
            'R►':"4",
            'W◁':"1",
            'W△':"1",
            'R▼':"4",
            'W▷':"1",
            'R◄':"4",
            'R▲':"4",
            'W▽':"1",
            'R▷':"3",
            'W◄':"2",
            'W▲':"2",
            'R▽':"3",
            'W►':"2",
            'R◁':"3",
            'R△':"3",
            'W▼':"2",
        }[sym]

    def b_board(self, board):
        return [[self.bins(e) for e in col] for col in board]

    def bins(self, string):
        return "1" if string != "0" else "0"
