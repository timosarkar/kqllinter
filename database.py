import sqlite3

DB_NAME = "chess.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO moves (from_pos, to_pos, piece, color) VALUES (?, ?, ?, ?)",
        (str(from_pos), str(to_pos), piece, color)
    )
    conn.commit()
    conn.close()
