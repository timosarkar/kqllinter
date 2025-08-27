import asyncio
import websockets
import os

# Paths
OPENINGS_FILE = "a.tsv"

# Initial board in FEN
initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Load openings from TSV
openings = {}
if os.path.exists(OPENINGS_FILE):
    with open(OPENINGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            eco, name, pgn = line.strip().split("\t")
            moves = " ".join([m for m in pgn.split() if not m.endswith('.')]).strip()
            openings[moves] = (eco, name)
else:
    print(f"Warning: {OPENINGS_FILE} not found. Opening detection disabled.")

# Board utilities
def fen_to_board(fen):
    board = []
    rows = fen.split()[0].split("/")
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(['.'] * int(char))
            else:
                board_row.append(char)
        board.append(board_row)
    return board

def board_to_fen(board, turn='w'):
    fen_rows = []
    for row in board:
        count = 0
        fen_row = ""
        for cell in row:
            if cell == '.':
                count += 1
            else:
                if count > 0:
                    fen_row += str(count)
                    count = 0
                fen_row += cell
        if count > 0:
            fen_row += str(count)
        fen_rows.append(fen_row)
    fen_board = "/".join(fen_rows)
    return f"{fen_board} {turn} - - 0 1"

# Minimal move validation (just basic coordinates)
def is_valid_coord(move):
    if len(move) != 4:
        return False
    src_col, src_row, dst_col, dst_row = move
    return src_col in 'abcdefgh' and dst_col in 'abcdefgh' and src_row in '12345678' and dst_row in '12345678'

# Convert coordinate move to basic SAN (MVP)
def coord_to_san(board, move):
    src_col = ord(move[0]) - ord('a')
    src_row = 8 - int(move[1])
    dst_col = ord(move[2]) - ord('a')
    dst_row = 8 - int(move[3])
    piece = board[src_row][src_col]
    target = board[dst_row][dst_col]
    
    if piece.lower() == 'p':
        san = move[2:4]  # e2e4 -> e4
        if target != '.':
            san = move[0] + 'x' + move[2:4]
    else:
        piece_letter = piece.upper() if piece.isupper() else piece.lower()
        piece_letter = piece_letter.upper() if piece_letter != 'P' else ''
        san = piece_letter + ('' if target == '.' else 'x') + move[2:4]
    
    # Castling
    if piece.upper() == 'K' and abs(dst_col - src_col) == 2:
        san = 'O-O' if dst_col > src_col else 'O-O-O'
    return san

def make_move(board, move):
    src_col = ord(move[0]) - ord('a')
    src_row = 8 - int(move[1])
    dst_col = ord(move[2]) - ord('a')
    dst_row = 8 - int(move[3])
    board[dst_row][dst_col] = board[src_row][src_col]
    board[src_row][src_col] = '.'

def detect_opening(current_san):
    played = " ".join(current_san)
    best_match = None
    for pgn, (eco, name) in openings.items():
        if played.startswith(pgn):
            best_match = (eco, name)
    return best_match

# Globals
clients = set()
board = fen_to_board(initial_fen)
turn = 'w'
current_san = []

async def broadcast_board():
    fen = board_to_fen(board, turn)
    board_str = "\n".join([" ".join(row) for row in board])
    opening = detect_opening(current_san)
    opening_str = f"OPENING: {opening[0]} {opening[1]}" if opening else "OPENING: Unknown"
    for client in clients:
        try:
            await client.send(f"BOARD\n{board_str}\nFEN: {fen}\nTURN: {turn}\n{opening_str}")
        except:
            pass

async def handle_client(websocket):
    global turn
    clients.add(websocket)
    try:
        await broadcast_board()
        async for message in websocket:
            move = message.strip()
            try:
                if is_valid_coord(move):
                    san = coord_to_san(board, move)
                    make_move(board, move)
                    current_san.append(san)
                    turn = 'b' if turn == 'w' else 'w'
                    await broadcast_board()
                else:
                    await websocket.send(f"INVALID MOVE: {move}")
            except Exception as e:
                await websocket.send(f"ERROR: {e}")
                print("Server error:", e)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())

