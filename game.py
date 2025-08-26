from board import initial_board
from board import King

class Game:
    def __init__(self):
        self.board = initial_board()
        self.turn = 'white'
        self.history = []

    def valid_moves(self, pos):
        piece = self.board.get(pos)
        if piece is None or piece.color != self.turn:
            return []
        moves = piece.moves(self.board, pos)
        # Filter moves that leave king in check
        valid = []
        for mv in moves:
            temp_board = self.board.copy()
            temp_board[mv] = piece
            del temp_board[pos]
            if not self.is_in_check(temp_board, self.turn):
                valid.append(mv)
        return valid

    def move(self, from_pos, to_pos):
        piece = self.board.get(from_pos)
        if piece is None or piece.color != self.turn:
            return False
        if to_pos not in self.valid_moves(from_pos):
            return False
        self.board[to_pos] = piece
        del self.board[from_pos]
        self.history.append((from_pos, to_pos, piece))
        self.turn = 'black' if self.turn == 'white' else 'white'
        return True

    def find_king(self, board, color):
        for pos, piece in board.items():
            if isinstance(piece, King) and piece.color == color:
                return pos
        return None

    def is_in_check(self, board, color):
        king_pos = self.find_king(board, color)
        if king_pos is None:
            return True  # King missing = checkmate
        for pos, piece in board.items():
            if piece.color != color:
                if king_pos in piece.moves(board, pos):
                    return True
        return False

    def is_checkmate(self):
        for pos, piece in self.board.items():
            if piece.color == self.turn:
                if self.valid_moves(pos):
                    return False
        return self.is_in_check(self.board, self.turn)
