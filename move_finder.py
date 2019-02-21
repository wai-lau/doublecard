class MoveFinder:
    def __init__(self, bs):
        self.bs = bs

    def open_spots(self, board):
        height = len(board[0])
        width = len(board)
        vertical_spots = []
        horizontal_spots = []
        for n, c in enumerate(board):
            h = int(len("".join(c)) / 2)
            if h < 11:
                vertical_spots.append((n,h))
            if (h < 12 and n < width - 1
                and not board[n + 1][h]
                and (h == 0 or board[n + 1][h - 1])):
                horizontal_spots.append((n,h))

        return vertical_spots, horizontal_spots

    def find_moves(self, board):
        v_spots, h_spots = self.open_spots(board)
        moves = ([self.generate_moves(v, "v") for v in v_spots] +
                 [self.generate_moves(h, "h") for h in h_spots])
        return [e for m in moves for e in m]

    def generate_moves(self, spot, orientation):
        moves = []
        vert = (2, 4, 6, 8)
        horz = (1, 3, 5, 7)

        rotations = (vert if orientation == "v" else horz)
        for i in rotations:
            moves.append([i, self.to_char(spot[0]), spot[1] + 1])
        return moves

    def to_char(self, col):
        return chr(col + 65)

    def find_recyclable(self, board, last_move):
        moves = []
        for c, col in enumerate(board):
            col_s = "".join(col)
            if not col_s:
                continue
            last_char = col_s[-1]
            height = int(len(col_s)/2)-1
            
            # ordering of remove_coord is guaranteed
            if last_char == '▷' or last_char == '▶':
                remove_coord = [self.to_char(c), height+1, self.to_char(c+1), height+1]
            elif last_char == '▽' or last_char == '▼':
                remove_coord = [self.to_char(c), height, self.to_char(c), height+1]
            else:
                continue

            remove_ds = self.bs.coord_to_dest(board, remove_coord)

            b = self.bs.copy(board)
            if self.bs.remove(
                b, remove_ds,
                last_move
            ):
                moves.extend(self.generate_recycle_moves(b, remove_coord, remove_ds))
        return moves

    def generate_recycle_moves(self, board, remove_coord, remove_ds):
        moves_after = self.find_moves(board)
        orientation = 0
        for i in range(1,9):
            dest_sym = self.bs.dest([i, 'A', 1])[0][2]
            if remove_ds[0][2] == dest_sym:
                orientation = i;
                break
        try:
            remove_card = [orientation, remove_coord[0], remove_coord[1]]
            moves_after.remove(remove_card)
        except ValueError:
            pass
        return list(map(lambda x: remove_coord + x, moves_after))

