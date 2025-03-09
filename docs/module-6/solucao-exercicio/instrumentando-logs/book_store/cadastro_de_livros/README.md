## API Cadastro de Livros

API para gerenciar cadastro de livros. Permite criar, buscar, listar e gerenciar o estoque de livros em uma base de dados.

## Endpoints

URL base: `http://localhost:8080`

### Adicionar livro

POST /livros/

Cria um novo livro no banco de dados.

Requisição:

- Body (JSON):
    ```json
    {
        "titulo": "string",
        "estoque": "number"
    }
    ```

Resposta:

- Status: 200 OK
    ```json
    {
        "id": "number",
        "titulo": "string",
        "estoque": "number"
    }
    ```
### Listar livros

GET /livros/

Lista todos os livros cadastrados no banco de dados.

Resposta:

- Status: 200 OK
    ```json
    [
        {
            "id": "number",
            "titulo": "string",
            "estoque": "number"
        }
    ]
    ```
### Buscar livro

GET /livros/{id}

Busca um livro pelo ID.

Parametros:

- `id` (int): ID do livro

Resposta:

- Status: 200 OK
    ```json
    {
        "id": "number",
        "titulo": "string",
        "estoque": "number"
    }
    ```

- Status: 404 Not Found
    ```json
    {
        "message": "Livro não encontrado"
    }
    ```
 
## Tratamento de Erros

Respostas de erro padrão:

- 404 Not Found: Recurso não encontrado.
- 500 Internal Server Error: Erro interno do servidor.
