"""
Contém as funções de manipulação de dados do banco de dados SQLite
"""
import sqlite3
from database import create_connection
from telemetry import logger

def save_pokemon(data):
    """
    Salva um novo Pokémon no banco de dados.
    """
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
            return True
    except sqlite3.IntegrityError as e:
        logger.error(f"Integrity error saving Pokemon: {e}")
        return False
    except sqlite3.Error as e:
        logger.error(f"Database error saving Pokemon: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error saving Pokemon: {e}")
        return False

def get_pokemon_by_name(name):
    """
    Busca um Pokémon pelo nome.
    """
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon WHERE name = ?", (name,))
            rows = cursor.fetchall()
            if rows:
                row = rows[0]
                return {
                    "id": row[0],
                    "name": row[1],
                    "height": row[2],
                    "weight": row[3],
                    "abilities": row[4].split(","),
                    "types": row[5].split(",")
                }
            return None
    except sqlite3.Error as e:
        logger.error(f"Error fetching Pokemon: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching Pokemon: {e}")
        return None

def list_pokemons():
    """
    Lista todos os Pokémons salvos no banco de dados SQLite.
    """
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon")
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "height": row[2],
                    "weight": row[3],
                    "abilities": row[4].split(","),
                    "types": row[5].split(",")
                }
                for row in rows
            ]
    except sqlite3.Error as e:
        logger.error(f"Error listing Pokemons: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error listing Pokemons: {e}")
        return []

def delete_pokemon_by_name(name):
    """
    Deleta um Pokémon pelo nome.
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
    except Exception as e:
        logger.error(f"Unexpected error deleting Pokemon: {e}")
        return False
