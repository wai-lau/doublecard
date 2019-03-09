from board_analyzer import BoardAnalyzer
from copy import deepcopy

class UselessAnalyzer(BoardAnalyzer):
    def analyze(self, board, token):
        board = deepcopy(board)
        for c, column in enumerate(board):
            for e, ele in enumerate(column):
                board[c][e] = ele.replace("►","X")\
                                 .replace("▼","X")\
                                 .replace("◄","X")\
                                 .replace("▲","X")\
                                 .replace("◁","O")\
                                 .replace("△","O")\
                                 .replace("▷","O")\
                                 .replace("▽","O")

        
        for c, column in enumerate(board):
            for e, ele in enumerate(column):
                if ele == "WO":
                    board[c][e] = c+1 + e*10
                elif ele == "WX":
                    board[c][e] = 3*(c+1 + e*10)
                elif ele == "RX":
                    board[c][e] = -2*(c+1 + e*10)
                elif ele == "RO":
                    board[c][e] = -1.5*(c+1 + e*10)

        return sum(sum(filter(lambda x: x, line))
                   for line in board)
