"""
Contém a lógica de negócio da aplicação incluindo validações e chamadas a API externas
"""
import requests
from flask import jsonify, request
from models import save_pokemon, get_pokemon_by_name, delete_pokemon_by_name, list_pokemons
from logs import logger
from traces import tracer

def fetch_pokemon_data(name):
    with tracer.start_as_current_span("fetch_pokemon_data") as span:
        span.set_attribute("pokemon.name", name)
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            pokemon_data = {
                "name": data.get("name"),
                "height": data.get("height"),
                "weight": data.get("weight"),
                "abilities": [ability["ability"]["name"] for ability in data.get("abilities", [])],
                "types": [type_data["type"]["name"] for type_data in data.get("types", [])]
            }
            save_pokemon(pokemon_data)
            return pokemon_data, 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Pokemon data: {e}")
            return None

def add_pokemon():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    try:
        data = request.get_json()
        required_fields = ["name", "height", "weight", "abilities", "types"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        save_pokemon(data)
        return jsonify({"message": "Pokemon added successfully"}), 201
    except Exception as e:
        logger.error(f"Error adding Pokemon: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

def get_pokemon(name):
    """
    Serviço para buscar um Pokemon pelo nome
    """
    try:
        pokemon = get_pokemon_by_name(name)
        if pokemon:
            return pokemon, 200
        else:
            return {"error": "Pokemon not found"}, 404
    except Exception as e:
        logger.error(f"Error fetching Pokemon: {e}")
        return {"error": "Internal Server Error"}, 500

def delete_pokemon(name):
    """
    Serviço para deletar um Pokemon pelo nome
    """
    try:
        if delete_pokemon_by_name(name):
            return {"message": "Pokemon deleted successfully"}, 200
        else:
            return {"error": "Pokemon not found"}, 404
    except Exception as e:
        logger.error(f"Error deleting Pokemon: {e}")
        return {"error": "Internal Server Error"}, 500
