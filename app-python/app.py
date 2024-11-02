from telemetry import logger
from flask import Flask, jsonify, request
from services import fetch_pokemon_data, add_pokemon, list_pokemons, get_pokemon, delete_pokemon

app = Flask(__name__)

@app.route("/pokemon/fetch/<name>", methods=["GET"])
def fetch_pokemon(name):
    logger.info(f"Fetching data for Pokemon: {name}")
    response, status_code = fetch_pokemon_data(name)
    return jsonify(response), status_code

@app.route("/pokemon", methods=["POST"])
def create_pokemon():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    logger.info("Adding a new Pokemon")
    return add_pokemon()

@app.route("/pokemon", methods=["GET"])
def list_all_pokemons():
    logger.info("Listing all Pokemon")
    pokemons = list_pokemons()
    return jsonify(pokemons)

@app.route("/pokemon/<name>", methods=["GET"])
def get_pokemon_route(name):
    logger.info(f"Fetching Pokemon from database: {name}")
    response, status_code = get_pokemon(name)
    return jsonify(response), status_code

@app.route("/pokemon/<name>", methods=["DELETE"])
def delete_pokemon_route(name):
    logger.info(f"Deleting Pokemon: {name}")
    response, status_code = delete_pokemon(name)
    return jsonify(response), status_code

if __name__ == "__main__":
    logger.info("* Starting Pokemon API server...")
    app.run(host="0.0.0.0", port=8080)
