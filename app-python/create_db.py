import sqlite3
from logs import logger

def create_database():
    """
    Cria o banco de dados SQLite para armazenar os pokemons
    """
    conn = sqlite3.connect("pokemon.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            height INTEGER,
            weight INTEGER,
            abilities TEXT,
            types TEXT
        );
    """)
    conn.commit()
    logger.info("Database created successfully")
    conn.close()

if __name__ == "__main__":
    logger.info("Creating database...")
    create_database()
