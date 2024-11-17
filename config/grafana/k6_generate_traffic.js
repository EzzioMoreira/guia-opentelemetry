import http from 'k6/http';
import { sleep } from 'k6';

// Configurações do teste
export const options = {
  stages: [
    { duration: '0s', target: 5 },    // Começa com 5 usuários
    { duration: '5m', target: 20 },   // Aumenta para 20 usuários ao longo de 5 minutos
    { duration: '5m', target: 30 },   // Aumenta para 30 usuários ao longo de 5 minutos
  ],
};

// Endpoint base
const BASE_URL = 'http://app:8080/pokemon';

// Lista de nomes de Pokémon
const POKEMONS = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch’d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Lickilicky", "Koffing", "Weezing", "Rhyhorn"];

// Função para obter um nome aleatório da lista
function getRandomName(list) {
  return list[Math.floor(Math.random() * list.length)];
}

// Função para buscar Pokémon na API externa
function fetchPokemon() {
  const pokemonName = getRandomName(POKEMONS);
  const response = http.get(`${BASE_URL}/fetch/${pokemonName}`);
  console.log(`Fetched Pokemon: ${pokemonName}, Status: ${response.status}`);
}

// Função para listar um Pokémon salvo
function getPokemonByName() {
  const pokemonName = getRandomName(POKEMONS);
  const response = http.get(`${BASE_URL}/${pokemonName}`);
  console.log(`Get Pokemon by Name: ${pokemonName}, Status: ${response.status}`);
}

// Função para listar todos os Pokémon salvos
function listAllPokemons() {
  const response = http.get(BASE_URL);
  console.log(`List all Pokemons, Status: ${response.status}`);
}

// Função para adicionar um Pokémon com nome aleatório
function addPokemonRandom() {
  const randomName = getRandomName(POKEMONS);
  const payload = JSON.stringify({
    name: randomName,
    height: (Math.random() * 2).toFixed(2), // Altura aleatória
    weight: (Math.random() * 100).toFixed(2), // Peso aleatório
    abilities: ['Run', 'Jump'],
    types: ['Normal'],
  });

  const headers = { 'Content-Type': 'application/json' };
  const response = http.post(BASE_URL, payload, { headers });
  console.log(`Added Pokemon: ${randomName}, Status: ${response.status}`);
}

// Função para deletar um Pokémon salvo
function deletePokemonByName() {
  const pokemonName = getRandomName(POKEMONS);
  const response = http.del(`${BASE_URL}/${pokemonName}`);
  console.log(`Deleted Pokemon: ${pokemonName}, Status: ${response.status}`);
}

// Função principal
export default function () {
  // Define os métodos disponíveis para o teste
  const actions = [
    () => fetchPokemon(),        // GET /fetch/{name}
    () => getPokemonByName(),    // GET /{name}
    () => listAllPokemons(),     // GET /
    () => addPokemonRandom(),    // POST /
    // () => deletePokemonByName(), // DELETE /{name}
  ];

  // Escolhe aleatoriamente uma ação
  const action = actions[Math.floor(Math.random() * actions.length)];
  action();

  // Dorme antes da próxima iteração
  sleep(0.5);
}
