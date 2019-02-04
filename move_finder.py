class MoveFinder:
    def open_spots(self, board):
        height = len(board[0])
        width = len(board)
        vertical_spots = []
        horizontal_spots = []
        for n, c in enumerate(board):
            h = int(len("".join(c))/2)
            if h < 11:
                vertical_spots.append((n,h))
            if (h < 12 and n < width-1
                and not board[n+1][h]
                and (h == 0 or board[n+1][h-1])):
                horizontal_spots.append((n,h))

        return vertical_spots, horizontal_spots

    def find_moves(self, board):
        v_spots, h_spots = self.open_spots(board)
        moves = ([self.generate_moves(v, "v") for v in v_spots] +
                 [self.generate_moves(h, "h") for h in h_spots])
        return [e for m in moves for e in m]

    def generate_moves(self, spot, orientation):
        moves = []
        vert = (2,4,6,8)
        horz = (1,3,5,7)

        rotations = (vert if orientation == "v" else horz)
        for i in rotations:
            moves.append("{}{}{}{}".format(
                "0", i, self.to_char(spot[0]), spot[1]+1)
            )
        return moves

    def to_char(self, col):
        return chr(col+65)
