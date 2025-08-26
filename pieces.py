class Piece:
    def __init__(self, color):
        self.color = color

    def moves(self, board, pos):
        return []

    def slides(self):
        return False


class Bishop(Piece):
    OFFSETS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    STEPS = 7

    def moves(self, board, pos):
        return self._slide_moves(board, pos)

    def slides(self):
        return True

    def _slide_moves(self, board, pos):
        moves = []
        x, y = pos
        for dx, dy in self.OFFSETS:
            for step in range(1, self.STEPS + 1):
                nx, ny = x + dx * step, y + dy * step
                if 1 <= nx <= 8 and 1 <= ny <= 8:
                    target = board.get((nx, ny))
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Rook(Piece):
    OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    STEPS = 7

    def moves(self, board, pos):
        return self._slide_moves(board, pos)

    def slides(self):
        return True

    def _slide_moves(self, board, pos):
        moves = []
        x, y = pos
        for dx, dy in self.OFFSETS:
            for step in range(1, self.STEPS + 1):
                nx, ny = x + dx * step, y + dy * step
                if 1 <= nx <= 8 and 1 <= ny <= 8:
                    target = board.get((nx, ny))
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Queen(Piece):
    OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    STEPS = 7

    def moves(self, board, pos):
        moves = []
        x, y = pos
        for dx, dy in self.OFFSETS:
            for step in range(1, self.STEPS + 1):
                nx, ny = x + dx * step, y + dy * step
                if 1 <= nx <= 8 and 1 <= ny <= 8:
                    target = board.get((nx, ny))
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def slides(self):
        return True


class Knight(Piece):
    OFFSETS = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def moves(self, board, pos):
        moves = []
        x, y = pos
        for dx, dy in self.OFFSETS:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= 8 and 1 <= ny <= 8:
                target = board.get((nx, ny))
                if target is None or target.color != self.color:
                    moves.append((nx, ny))
        return moves

    def slides(self):
        return False


class King(Piece):
    OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]

    def moves(self, board, pos):
        moves = []
        x, y = pos
        for dx, dy in self.OFFSETS:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= 8 and 1 <= ny <= 8:
                target = board.get((nx, ny))
                if target is None or target.color != self.color:
                    moves.append((nx, ny))
        return moves

    def slides(self):
        return False


class Pawn(Piece):
    def moves(self, board, pos):
        moves = []
        x, y = pos
        direction = 1 if self.color == 'white' else -1
        # Forward
        if (x + direction, y) not in board:
            moves.append((x + direction, y))
            # Double move
            if (self.color == 'white' and x == 2) or (self.color == 'black' and x == 7):
                if (x + 2 * direction, y) not in board:
                    moves.append((x + 2 * direction, y))
        # Captures
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            target = board.get((nx, ny))
            if target is not None and target.color != self.color:
                moves.append((nx, ny))
        return moves

    def slides(self):
        return False


PIECE_CLASSES = {
    'pawn': Pawn,
    'rook': Rook,
    'knight': Knight,
    'bishop': Bishop,
    'queen': Queen,
    'king': King
}
