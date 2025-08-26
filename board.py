from pieces import Pawn, Rook, Knight, Bishop, Queen, King

def initial_board():
    board = {}
    # Pawns
    for y in range(1, 9):
        board[(2, y)] = Pawn('white')
        board[(7, y)] = Pawn('black')
    # Rooks
    board[(1, 1)] = Rook('white')
    board[(1, 8)] = Rook('white')
    board[(8, 1)] = Rook('black')
    board[(8, 8)] = Rook('black')
    # Knights
    board[(1, 2)] = Knight('white')
    board[(1, 7)] = Knight('white')
    board[(8, 2)] = Knight('black')
    board[(8, 7)] = Knight('black')
    # Bishops
    board[(1, 3)] = Bishop('white')
    board[(1, 6)] = Bishop('white')
    board[(8, 3)] = Bishop('black')
    board[(8, 6)] = Bishop('black')
    # Queens
    board[(1, 4)] = Queen('white')
    board[(8, 4)] = Queen('black')
    # Kings
    board[(1, 5)] = King('white')
    board[(8, 5)] = King('black')
    return board
