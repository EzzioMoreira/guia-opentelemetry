## API Ordem de Compra

API para gerenciar ordens de compra de livros. Permite criar e buscar ordens de compra.

## Endpoints

URL base: `http://localhost:8081`

### Criar Ordem de Compra

POST /ordens

Cria uma nova ordem de compra no banco de dados.

Requisição:

- Body (JSON):
    ```json
    {
        "id_livro": "number"
    }
    ```

Resposta:

- Status: 200 OK
    ```json
    {
        "id": "number",
        "id_livro": "number",
        "status": "string"
    }
    ```

### Buscar Ordem de Compra

GET /ordens/{id}

Busca uma ordem de compra pelo ID.

Parâmetros:

- `id` (int): ID da ordem de compra

Resposta:

- Status: 200 OK
    ```json
    {
        "id": "number",
        "id_livro": "number",
        "status": "string"
    }
    ```

- Status: 404 Not Found
    ```json
    {
        "message": "Ordem não encontrada"
    }
    ```

## Tratamento de Erros

Respostas de erro padrão:

- 404 Not Found: Recurso não encontrado.
- 500 Internal Server Error: Erro interno do servidor.
