## Instrumentação Sem Código

Também conhecido como Auto-Instrumentação, é o processo em que o OpenTelemetry modifica o comportamento da aplicação em tempo de execução, adicionando código para gerar dados de telemetria métricas, traces e logs. A instrumentação sem código é a maneira mais fácil e rápida de adicionar telemetria em aplicações sem a necessidade de alterar o código fonte.

O mecanismo de instrumentação sem código do OpenTelemetry pode variar de acordo com a linguagem de programação, variando entre as manipulação de bytecode, monkey patching ou eBPF que injeta chamadas para API e o SDK do OpenTelemetry no aplicativo. 

Através do processo de instrumentação sem código, toda vez que uma requisição é feita na aplicação o OpenTelemetry captura e envia a telemetria para o OpenTelemetry Collector, que por sua vez, envia para ferramenta de visualização de telemetria como Datadog, Grafana, Newrelic, Dynatrace entre outras.

Como mencionado anteriormente, a instrumentação sem código é um bom começo para iniciar sua jornada com instrumentação de aplicações, mas é importante lembrar que a instrumentação sem código não é suficiente para todos os cenários. Em alguns casos, você terá que mesclar com a instrumentação manualmente (instrumentação com código) para ter dados de telemetria corretos da aplicação.

## Implementando Instrumentação Sem Código

Agora, siga estes passos para implementar a instrumentação sem código na aplicação Python [BookStore](aplicação-de-exemplo.md). A telemetria emitida pela aplicação após a instrumentação será enviada para o OpenTelemetry Collector e visualizada na Stack Grafana.

1. Clonar o repositório e acessar o diretório do módulo:

   ```bash
    git clone https://github.com/EzzioMoreira/treinamento-opentelemetry.git && cd treinamento-opentelemetry
    ```

    Dentro do diretório `treinamento-opentelemetry`, existe o diretório [book_store](../../book_store/) que contém a aplicação de exemplo.

    - [Cadastro de Livros](../../book_store/cadastro_de_livros/).
    - [Ordem de Compra](../../book_store/ordem_de_compra/).
    - [Pagamento](../../book_store/pagamento/).

1. Para implementar a instrumentação sem código, adicione os pacotes `opentelemetry-distro` e `opentelemetry-exporter-otlp` ao arquivo [requirements.txt](../../book_store/cadastro_de_livros/requirements.txt) do microserviço `Cadastro de Livro`.

    ```shell
    opentelemetry-distro==0.49b2
    opentelemetry-exporter-otlp==1.28.2
    opentelemetry-instrumentation-fastapi==0.49b2
    ```

    O conteúdo do arquivo `requirements.txt` deve ser semelhante ao exemplo abaixo:

    ```shell
    fastapi==0.109.1
    uvicorn==0.15.0
    sqlalchemy==2.0.32
    sqlalchemy-utils==0.41.2
    psycopg2-binary==2.9.10
    requests==2.31.0
    opentelemetry-distro==0.49b2
    opentelemetry-exporter-otlp==1.28.2
    opentelemetry-instrumentation-fastapi==0.49b2
    ```

    O [pacote OpenTelemetry distro](https://opentelemetry.io/docs/languages/python/distro/) fornece os mecanismos para configurar automaticamente as opções mais comuns para a instrumentação, como a definição para o `SDK TraceProvider`, `BatchSpanProcessor` e `OTLP SpanExporter`.
    
    O `opentelemetry-exporter-otlp` é um exportador que envia os dados de telemetria para o OpenTelemetry Collector ou qualquer outro [endpoint OTLP](https://opentelemetry.io/docs/specs/otel/protocol/exporter/).
    
1. O Próximo passo será adicionar o pacote `opentelemetry-bootstrap` ao arquivo [Dockerfile](../../book_store/cadastro_de_livros/Dockerfile) do microserviço `Cadastro de Livro`.

    ```shell
    RUN opentelemetry-bootstrap -a install
    ```
    > Existe um comentário no arquivo `Dockerfile` que indica onde adicionar o trecho de código.
    
    O [opentelemetry-bootstrap](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/opentelemetry-instrumentation#opentelemetry-bootstrap) faz a leitura dos pacotes instalados na aplicação e instala as bibliotecas necessárias para instrumentar a aplicação. Por exemplo, estamos utilizando o pacote [FastAPI](https://fastapi.tiangolo.com/) o `opentelemetry-bootstrap` irá instalar o pacote `opentelemetry-instrumentation-fastapi` para instrumentar a aplicação.

    A lista completa de pacotes de instrumentação padrão e detectáveis está definida [aqui](https://github.com/open-telemetry/opentelemetry-python-contrib/blob/main/opentelemetry-instrumentation/src/opentelemetry/instrumentation/bootstrap_gen.py).

1. No `entrypoint` do [Dockerfile](../../book_store/cadastro_de_livros/Dockerfile) do microserviço `Cadastro de Livro`, adicione o prefixo `opentelemetry-instrument` ao comando de execução da aplicação. 

    > Existe um comentário no arquivo `Dockerfile` que indica onde adicionar o trecho de código.

    ```Dockerfile
    CMD ["opentelemetry-instrument",.....]
    ```

    O entrypoint do Dockerfile deve ser semelhante ao exemplo abaixo:

    ```Dockerfile
    CMD ["opentelemetry-instrument", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
    ```

    O comando [opentelemetry-instrument](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/opentelemetry-instrumentation#opentelemetry-instrument) tentará detectar automaticamente os pacotes usados na aplicação e, quando possível, aplicará a instrumentação. O comando suporta configurações adicionais, como a definição de um `tracer_exporter`, `metrics_exporter` entre outros, veja o exemplo.

    ```shell
    opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    --service_name your-service-name \
    --exporter_otlp_endpoint ip-otel-collector:4317 \
    python myapp.py
    ```

    Como alternativa, vamos utilizar variáveis de ambiente para configurar o `opentelemetry-instrument`. Para isso, adicione as seguintes variáveis de ambiente no arquivo [docker-compose.yaml](../../docker-compose.yaml) no microserviço `Cadastro de Livro`.

    > Existe um comentário no arquivo `docker-compose.yaml` que indica onde adicionar o trecho de código.

    ```yaml
    environment:
      - OTEL_SERVICE_NAME=cadastro_de_livros
      - OTEL_RESOURCE_ATTRIBUTES=service.version=v0.0.1,service.env=dev
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otelcollector:4317
      - OTEL_EXPORTER_OTLP_PROTOCOL=grpc
      - OTEL_EXPORTER_OTLP_INSECURE=true
      - OTEL_PYTHON_LOG_CORRELATION=true
    ```

    Estamos configurando o `OTEL_SERVICE_NAME` com o nome do serviço, `OTEL_RESOURCE_ATTRIBUTES` com os atributos do serviço, `OTEL_EXPORTER_OTLP_ENDPOINT` com o endpoint do OpenTelemetry Collector, `OTEL_EXPORTER_OTLP_INSECURE` para permitir conexões inseguras ao OpenTelemetry Collector e `OTEL_PYTHON_LOG_CORRELATION` para correlacionar os logs com as traces, nesse caso o `TRACE_ID` e `SPAN_ID` serão adicionados como campos no log.

    Para mais informações sobre as variáveis de ambiente, consulte a documentação do [OpenTelemetry](https://opentelemetry.io/docs/languages/sdk-configuration/general/)

1. Pronto! Agora, basta executar o comando `docker-compose up` para iniciar a aplicação.

    ```shell
    docker-compose up
    ```

1. Acesse os endpoints da aplicação para gerar dados de telemetria:

    Ao acessar o endpoint, a aplicação irá listar todos os livros cadastrados.

    ```shell
    curl http://localhost:8080/livros/
    ```

    Ao acessar o endpoint, a aplicação irá adicionar um novo livro ao banco de dados.

    ```shell
    curl -X POST http://localhost:8080/livros/ -H "Content-Type: application/json" -d '{"titulo": "A Força do Vento", "estoque": 10}'

    curl -X POST http://localhost:8080/livros/ -H "Content-Type: application/json" -d '{"titulo": "A Força do Sol", "estoque": 20}'
    
    curl -X POST http://localhost:8080/livros/ -H "Content-Type: application/json" -d '{"titulo": "A Força da Chuva", "estoque": 0}'
    ```

    Ao acessar o endpoint, a aplicação irá buscar os detalhes de um livro específico pelo ID.

    ```shell
    curl -X GET http://localhost:8080/livros/<id>
    ```
    > Substitua `<id>` pelo ID do livro que deseja buscar.

    Ao acessar o endpoint, a aplicação irá retornar todos os livros cadastrados.

    ```shell
    curl -X GET http://localhost:8080/livros/
    ```

    Dica: você pode utilizar o Swagger para testar os endpoints da aplicação. 
    Acesse http://localhost:8080/docs para visualizar a documentação dos endpoints.

    ![Swagger](./image/zero-code/zero-code-swagger.png)

1. Acesse o Grafana para visualizar a telemetria gerada em http://localhost:3000.

    No menu `explorer` do Grafana, você pode visualizar as métricas, traces e logs. Selecione `service.name` = `cadastro-de-livros` para visualizar a telemetria gerada pela aplicação.

### O Que Esperar?

Quando você acessar os endpoints da aplicação, o OpenTelemetry irá capturar as requisições e enviar para o OpenTelemetry Collector. O OpenTelemetry Collector irá processar e enviar a telemetria para Tempo, Prometheus e Loki. Por fim, você poderá visualizar a telemetria no Grafana.

#### Trace

A imagem a seguir mostra um exemplo de trace gerado pela aplicação Python.

![Trace](./image/zero-code/zero-code-trace.png)

#### Métricas

A imagem a seguir mostra um exemplo de métricas geradas pela aplicação Python.

![Métricas](./image/zero-code/zero-code-metric.png)

#### Logs

A imagem a seguir mostra um exemplo de logs gerados pela aplicação Python.

![Logs](./image/zero-code/zero-code-log.png)

## Exercício

Agora que você implementou a instrumentação sem código na aplicação Cadastro de Livros, implemente a instrumentação sem código nas aplicações [Ordem de Compra](../../book_store/ordem_de_compra/) e [Pagamento](../../book_store/pagamento/).

1. Adicione os pacotes `opentelemetry-distro` e `opentelemetry-exporter-otlp` ao arquivo `requirements.txt` das aplicações `Ordem de Compra` e `Pagamento`.
1. Adicione o pacote `opentelemetry-bootstrap` ao arquivo `Dockerfile` das aplicações `Ordem de Compra` e `Pagamento`.
1. Adicione o prefixo `opentelemetry-instrument` ao comando de execução da aplicação no `entrypoint` do arquivo `Dockerfile` das aplicações `Ordem de Compra` e `Pagamento`.
1. Adicione as variáveis de ambiente no arquivo `docker-compose.yaml` das aplicações `Ordem de Compra` e `Pagamento`.

> Dica: Utilize o comando `docker-compose up --build` para reconstruir as imagens das aplicações `Ordem de Compra` e `Pagamento`.

### Resultado Esperado

Após implementar a instrumentação sem código nas aplicações `Cadastro de Livros`, `Ordem de Compra` e `Pagamento`, você deve ser capaz de visualizar o trace gerado pelas aplicações no Grafana e seu ciclo de vida.

A imagem a seguir mostra um exemplo do trace após criar uma ordem de compra e realizar o pagamento.

![Trace](./image/zero-code/zero-code-all-instrument.png)

## Conclusão

A instrumentação sem código é uma maneira fácil e rápida de adicionar telemetria em aplicações sem a necessidade de alterar o código fonte.

A técnica utilizada para gerar a telemetria sem código é conhecida como Monkey Patching, onde as chamadas feitas pelo o aplicativo para as biblioteca são interceptadas sem que o código original seja alterado. No caso do FastAPI, a biblioteca `opentelemetry-instrumentation-fastapi` aplica o Monkey Patching sobre as funções internas do framework. Isso permite gerar métricas e traces automaticamente antes de chamar a biblioteca subjacente.

| **FastAPI App Layer** (Requisição do Usuário) | **OpenTelemetry Instrumenting Layer** (Interceptação e Monitoramento) | **FastAPI Library Layer** (Execução Final) |
|--------------------------------|--------------------------------------------------|------------------------------|
| O usuário faz um request para `GET /livros/`. | OpenTelemetry intercepta a chamada e produz a telemetria. | FastAPI processa a requisição. |
| O código do FastAPI chama a rota correspondente. | OpenTelemetry injeta contexto nas requisição. | FastAPI executa a lógica da rota e retorna JSON. |
| FastAPI retorna a resposta HTTP. | OpenTelemetry finaliza e envia os dados de telemetria. | O cliente recebe a resposta da API. |

## Saiba Mais

- [OpenTelemetry Python](https://opentelemetry.io/docs/zero-code/)
- [Byte Buddy](https://bytebuddy.net/#/)
- [Monkey Patching](https://en.wikipedia.org/wiki/Monkey_patch)
- [Zero Code](https://opentelemetry.io/docs/concepts/instrumentation/zero-code/)
- [OpenTelemetry Enhancement Proposal (OTEP) - Similar a RFC](https://github.com/open-telemetry/opentelemetry-specification/tree/main/oteps/)
