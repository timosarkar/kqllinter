from flask import Flask, render_template, request, redirect
from game import Game
import sqlite3

def init_db():
    conn = sqlite3.connect("chess.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS moves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_pos TEXT,
            to_pos TEXT,
            piece TEXT,
            color TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_move(from_pos, to_pos, piece, color):
    conn = sqlite3.connect("chess.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO moves (from_pos, to_pos, piece, color) VALUES (?, ?, ?, ?)",
        (str(from_pos), str(to_pos), piece, color)
    )
    conn.commit()
    conn.close()


app = Flask(__name__)
game = Game()
init_db()

FILES = 'abcdefgh'

def pos_to_coord(pos):
    row, col = pos
    return f"{FILES[col-1]}{row}"

def coord_to_pos(coord):
    try:
        col = FILES.index(coord[0].lower()) + 1
        row = int(coord[1])
        if 1 <= row <= 8 and 1 <= col <= 8:
            return (row, col)
    except:
        return None
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    global game
    msg = ""
    if request.method == "POST":
        move_input = request.form.get("move", "").replace(" ", "").lower()
        if len(move_input) == 4:
            from_coord = move_input[:2]
            to_coord = move_input[2:]
            from_pos = coord_to_pos(from_coord)
            to_pos = coord_to_pos(to_coord)
            piece = game.board.get(from_pos)
            if from_pos and to_pos and piece:
                if game.move(from_pos, to_pos):
                    log_move(from_pos, to_pos, piece.__class__.__name__, piece.color)
                    if game.is_checkmate():
                        msg = f"Checkmate! {game.turn.capitalize()} loses!"
                else:
                    msg = '<div class="error-message">invalid move</div><br>'
            else:
                msg = '<div class="error-message">invalid move</div><br>'
        else:
            msg = '<div class="error-message">invalid move</div><br>'

    return render_template("index.html", board=game.board, msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
