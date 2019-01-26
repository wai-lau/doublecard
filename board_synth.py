from colorama import Fore, Back, Style
from copy import deepcopy
# coordinates are board[column][row]
# bottom left block is (A,0)

class BoardSynth:
    def apply(self, board, *cards):
        # this could be something to take out if we don't need rollbacks
        board_original = deepcopy(board)
        for c in cards:
            ds = self.dest(c)
            if ds and self.legal(board, ds):
                for s in ds:
                    board[s[0]][s[1]] = s[2]
            else:
                print("Illegal move: "+c)
                board = board_original
                return False
        return True

    def legal(self, board, dest):
        for i, d in enumerate(dest):
            e, r = d[0], d[1]
            if r < 0 or len(board[0]) < r:
                return False
            if e < 0 or len(board) < e:
                return False
            if board[e][r]:
                return False
            # because we are only checking directly below,
            # there is the constraint that
            # we need to keep the order of the cards played

            # if second piece is above first
            # then we only need to check the first piece
            if i == 0 or r == dest[0][1]:
                if r is not 0:
                    if not board[e][r-1]:
                        return False
        return True

    def to_n(self, char):
        return ord(char.upper())-65

    def dest(self, card):
        orientation = int(card[1])
        e = int(self.to_n(card[2]))
        r = int(card[3])-1
        if orientation == 1:
            return ((e, r, 'R▶'), (e+1, r, 'W◁'))
        if orientation == 2:
            return ((e, r, 'W△'), (e, r+1, 'R▼'))
        if orientation == 3:
            return ((e, r, 'W▷'), (e+1, r, 'R◀'))
        if orientation == 4:
            return ((e, r, 'R▲'), (e, r+1, 'W▽'))
        if orientation == 5:
            return ((e, r, 'R▷'), (e+1, r, 'W◀'))
        if orientation == 6:
            return ((e, r, 'W▲'), (e, r+1, 'R▽'))
        if orientation == 7:
            return ((e, r, 'W▶'), (e+1, r, 'R◁'))
        if orientation == 8:
            return ((e, r, 'R△'), (e, r+1, 'W▼'))

    def render(self, board):
        t_board = zip(*board)
        for r, row in reversed(list(enumerate(t_board))):
            print(Back.BLACK + Fore.WHITE + str(r+1) + (2-int(r/10))*' ' +
                  "".join([self.to_symbol(e) for e in row]))
        print(Back.BLACK + Fore.WHITE + '   ABCDEFGH'+Style.RESET_ALL)

    def to_symbol(self, string):
        if not string:
            return Back.BLACK + ' '

        bg = fg = None
        if string[0].upper() == 'W':
            bg = Back.WHITE
        else:
            bg = Back.RED
        fg = Fore.BLACK + string[1]

        return bg + fg

    def new(width = 8, height = 12):
        width, height = 8, 12
        return [['' for _ in range(height)] for _ in range(width)]
