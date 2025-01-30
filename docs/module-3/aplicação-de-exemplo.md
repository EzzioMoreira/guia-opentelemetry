## Sistema Bookstore

Durante o treinamento de OpenTelemetry, vamos utilizar um sistema de exemplo chamado Bookstore. O sistema Bookstore é formado por microserviços que são responsáveis por gerenciar cadastro de livros, ordem de compras e pagamento.

O sistema foi projetado para simular um cenário real de microserviços, proporcionando uma experiência prática para instrumentação de aplicações com OpenTelemetry.

### Microserviços

- Tecnologias Utilizadas
    - Linguagem: Python 3.12
    - Banco de Dados: PostgreSQL

- Cadastro de Livros: Serviço responsável por gerenciar o cadastro de livros.
- Ordem de Compra: Serviço responsável por gerenciar a ordem de compra de livros.
- Pagamento: Serviço responsável por gerenciar o pagamento da ordem de compra.

### Diagrama de Arquitetura

Sistema Bookstore é formado por três microserviços:

```mermaid
graph TD
    subgraph Pagamento
        C1[POST /pagamentos]
        C2[GET /pagamentos/id]
        DB3[(Banco de Dados)]
        C1 --> DB3
        C2 --> DB3
    end

    subgraph Ordem_de_Compra
        A1[POST /ordens] --> A2[Validação no Cadastro de Livros]
        A2 --> A3[Chamada ao Serviço de Pagamento]
        A3 --> A4[Registro da Compra no Banco de Dados]
        DB1[(Banco de Dados)]
        A4 --> DB1
    end

    subgraph Cadastro_de_Livros
        B1[POST /livros]
        B2[GET /livros]
        B3[GET /livros/id]
        DB2[(Banco de Dados)]
        B1 --> DB2
        B2 --> DB2
        B3 --> DB2
    end

    %% Comunicação entre os serviços
    A2 -- "Valida Estoque" --> B3
    A3 -- "Processar Pagamento" --> C1
    C1 -- "Atualizar status de pagamento" --> A4
```

### Diagrama de Sequência

O diagrama de sequência a seguir mostra a interação entre os microserviços do sistema Bookstore:

1. O cliente Inicia o processo de compra.
    - Cliente envia uma requisição para o serviço Ordem_de_Compra para criar uma ordem de compra.
2. Valida Disponibilidade de Estoque.
    - O serviço Ordem_de_Compra valida a disponibilidade de estoque chamando o serviço Cadastro_de_Livros.
3. Processa Pagamento.
    - Após a validação do estoque, o serviço Ordem_de_Compra chama o serviço Pagamento para processar o pagamento.
4. Atualiza Status da Ordem.
    - O serviço Pagamento retorna o status do pagamento para o serviço Ordem_de_Compra, que atualiza o status da ordem de compra.

```mermaid
sequenceDiagram
    participant Cliente
    participant Ordem_de_Compra
    participant Cadastro_de_Livros
    participant Pagamento

    Cliente->>Ordem_de_Compra: POST /ordens (Criar Ordem)
    Ordem_de_Compra->>Cadastro_de_Livros: GET /livros/{id} (Validar Estoque)
    Cadastro_de_Livros-->>Ordem_de_Compra: Estoque Disponível ou Indisponível
    Ordem_de_Compra->>Pagamento: POST /pagamentos (Processar Pagamento)
    Pagamento-->>Ordem_de_Compra: Status do Pagamento (Aprovado/Recusado)
    Ordem_de_Compra-->>Cliente: Status da Ordem (Concluída/Não Concluída)
```
