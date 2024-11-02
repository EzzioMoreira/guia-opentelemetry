# Pokemon API Treinamento OpenTelemetry

API para treinamento de OpenTelemetry, com funcionalidades para buscar dados de Pokemon em uma API externa e salvar no banco de dados.

## Endpoints

### Buscar Pokemon na API externa e salvar no banco

- **Endpoint**: `/pokemon/fetch/<name>`
- **Método**: `GET`
- **Descrição**: Busca dados de um Pokemon na API externa e salva no banco de dados.

### Listar Pokemon salvos no banco por nome

- **Endpoint**: `/pokemon/<name>`
- **Método**: `GET`
- **Descrição**: Lista Pokemon salvos no banco de dados por nome.

### Listar todos Pokemon salvos no banco

- **Endpoint**: `/pokemon`
- **Método**: `GET`
- **Descrição**: Lista todos Pokemon salvos no banco de dados.

### Adicionar Pokemon no banco

- **Endpoint**: `/pokemon`
- **Método**: `POST`
- **Descrição**: Adiciona um Pokemon no banco de dados.
- **Corpo da requisição**:
  - Content-Type: application/json
  ```json
  {
    "name": "string",
    "height": "number",
    "weight": "number",
    "base_experience": "number"
  }
  ```

### Delete Pokemon do banco

- **Endpoint**: `/pokemon/<name>`
- **Método**: `DELETE`
- **Descrição**: Deleta um Pokemon no banco de dados.
