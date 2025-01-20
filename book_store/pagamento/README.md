# API Pagamento

API para gerenciar pagamentos de ordens de compra. Permite processar e consultar pagamentos.

---

## Endpoints

**URL base**: `http://localhost:8082`

---

### Processar Pagamento

**POST /pagamentos**

Processa o pagamento de uma ordem de compra e registra o status do pagamento.

#### Requisição

- **Body (JSON)**:
    ```json
    {
        "id_ordem": "number",
    }
    ```

#### Resposta

- **Status: 200 OK**
    ```json
    {
        "id": "number",
        "id_ordem": "number",
        "status": "string"
    }
    ```

### Consultar Pagamento

**GET /pagamentos/{id}**

Consulta os detalhes de um pagamento pelo ID.

#### Parâmetros

- `id` (int): ID do pagamento.

#### Resposta

- **Status: 200 OK**
    ```json
    {
        "id": "number",
        "id_ordem": "number",
        "status": "string"
    }
    ```

- **Status: 404 Not Found**
    ```json
    {
        "message": "Pagamento não encontrado"
    }
    ```

---

## Tratamento de Erros

Respostas de erro padrão:

- **404 Not Found**: Recurso não encontrado.
- **500 Internal Server Error**: Erro interno do servidor.

---

## Notas Adicionais

- O status de um pagamento pode ser um dos seguintes valores:
  - `Aprovado`: O pagamento foi processado com sucesso.
  - `Recusado`: O pagamento foi recusado pelo sistema.
