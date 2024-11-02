"""
Contém as funções de manipulação de dados do banco de dados SQLite
"""
from database import create_connection
from telemetry import logger

def save_pokemon(data):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pokemon (name, height, weight, abilities, types)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data.get("name"),
                data.get("height"),
                data.get("weight"),
                ",".join(data.get("abilities", [])),
                ",".join(data.get("types", []))
            ))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error saving Pokemon: {e}")

def get_pokemon_by_name(name):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon WHERE name = ?", (name,))
            rows = cursor.fetchall()
            if rows:
                row = rows[0]
                return {"id": row[0], "name": row[1], "height": row[2], "weight": row[3], "abilities": row[4].split(","), "types": row[5].split(",")}
            return None
    except sqlite3.Error as e:
        logger.error(f"Error fetching Pokemon: {e}")
        return None

def list_pokemons():
    """
    Lista todos os pokemons salvos no banco de dados SQLite
    """
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon")
            rows = cursor.fetchall()
            return [
                {"id": row[0], "name": row[1], "height": row[2], "weight": row[3], "abilities": row[4].split(","), "types": row[5].split(",")}
                for row in rows
            ]
    except sqlite3.Error as e:
        logger.error(f"Error listing Pokemons: {e}")
        return None

def delete_pokemon_by_name(name):
    """
    Deleta um pokemon pelo nome no banco de dados SQLite
    """
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pokemon WHERE name = ?", (name,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            return False
    except sqlite3.Error as e:
        logger.error(f"Error deleting Pokemon: {e}")
        return False
