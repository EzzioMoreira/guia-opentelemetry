import sqlite3
import logs as logger

def create_connection():
    """
    Cria uma conexão com o banco de dados SQLite
    """
    try:
        conn = sqlite3.connect("pokemon.db")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None
