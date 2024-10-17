## Instrumentação Manual

A instrumentação manual é o processo de adicionar código em aplicações para gerar dados de telemetria. A instrumentação manual é feita utilizando APIs e SDKs do OpenTelemetry.

> A instrumentação manual é recomendada para cenários em que a instrumentação sem código não é suficiente.

### Implementando Instrumentação Manual

1. Clonar o repositório e acessar o diretório do módulo:

   ```bash
    git clone https://github.com/EzzioMoreira/treinamento-opentelemetry.git
    cd treinamento-opentelemetry/docs/Modulo-2\ -\ OpenTelemetry
    ```

1. Primeiro, precisamos instalar as bibliotecas necessárias para adicionar instrumentação. Adicione os seguintes pacotes ao arquivo `requirements.txt`:

   ```txt
   opentelemetry-api
   opentelemetry-sdk
   opentelemetry-exporter-otlp
   ```

1. Para iniciar a instrumentação, é necessário instanciar o `TracerProvider`, responsável por gerenciar `Traces` e `Spans`. Diversos Spans agrupados formam um Trace. A configuração inicial também inclui a as classes `OTLPSpanExporter` e `BatchSpanProcessor` para configurar o Trace Provider. Adicione o seguinte trecho de código ao arquivo `app.py`:

    ```python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    provider = TracerProvider()
    span_exporter = OTLPSpanExporter()
    processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    ```

    Com a pipeline de rastreamento configurada, podemos obter um Tracer. A interface do `TraceProvider` define um método `get_tracer` que nos permite obter um `Tracer`. O método requer um nome e opcionalmente uma versão. Isso é útil para identificar a origem e a versão do rastreamento.

1. Agora, podemos adicionar spans nas funções onde desejamos rastrear o fluxo de execução. Use o trecho de código a seguir para adicionar spans na função `fetch_data_from_external_service`.

    ```python
    def fetch_data_from_external_service():
        with tracer.start_as_current_span("fetch_data_from_external_service") as span:
            # Simula uma solicitação HTTP GET para um serviço externo
            response = requests.get("http://httpbin.org/get")
            sleep(latency)
            logging.info(f"GET request to httpbin.org returned {response.status_code}")
            span.end()
            return f"GET request to httpbin.org returned {response.status_code}"
    ```

    Quando definimos `start_as_current_span`, estamos criando um novo span e definindo-o como o span ativo. Isso significa que qualquer operação que ocorra dentro do bloco `with` será associada a esse span.

    Uma vez que a função retorna o resultado da solicitação, o método `end` é chamado para finalizar o span. É uma boa prática chamar o método `end` para garantir que o span seja finalizado corretamente.

1. Definia as variáveis de ambiente necessárias para configurar o `OTLPSpanExporter`. Adicione o seguinte trecho de código ao arquivo `docker-compose.yaml`:

    ```yaml
    environment:
      - OTEL_SERVICE_NAME=app-python
      - OTEL_RESOURCE_ATTRIBUTES=service.name=app-python, service.version=1.0.0, service.env=dev
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otelcollector:4317
      - OTEL_EXPORTER_OTLP_INSECURE=true
      - OTEL_PYTHON_LOG_CORRELATION=true
    ```

    - Em seguida, execute o comando `docker-compose up` para iniciar a aplicação.

    ```shell
    docker-compose up
    ```

    - Acessar os endpoints da aplicação para gerar traces: [http://localhost:8080/fetch-data](http://localhost:8080/fetch-data) em seguida, acesse o Grafana para visualizar a telemetria gerada [http://localhost:3000](http://localhost:3000).

    Perceba que no Trace não há informações no Span Attributes, isso ocorre porque não definimos nenhum atributo no Span. Chegaremos nesse ponto mais adiante.

    ![Trace](./image/trace3.5.png)

1. Vamos enriquecer o Trace adicionando atributos ao Span. Usaremos [Atributos Semânticos](https://opentelemetry.io/docs/specs/semconv/general/trace/) que permite a normalização dessas informações. Primeiro é necessário instalar o pacote `opentelemetry-semantic-conventions`, adicione o pacote ao arquivo `requirements.txt`:

    ```txt
    ...
    opentelemetry-semantic-conventions
    ...
    ```

    - Em seguida, importe o pacote:

    ```python
    from opentelemetry.semconv.trace import SpanAttributes
    ```

    - Adicione os atributos ao Span:

    ```python
    def fetch_data_from_external_service():
        def fetch_data_from_external_service():
        with tracer.start_as_current_span("fetch_data_from_external_service") as span:
            # Simula uma solicitação HTTP GET para um serviço externo
            response = requests.get("http://httpbin.org/get")
            # Adiciona atributos ao Span
            span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
            span.set_attribute(SpanAttributes.HTTP_FLAVOR, "1.1")
            span.set_attribute(SpanAttributes.HTTP_ROUTE, "/get")
            span.set_attribute(SpanAttributes.HTTP_URL, "http://httpbin.org")
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, response.status_code)
            sleep(latency)
            logging.info(f"GET request to httpbin.org returned {response.status_code}")
            span.end()
            return f"GET request to httpbin.org returned {response.status_code}"
    ```

    Atributos são pares de chave-valor que fornecem informações adicionais sobre o span. Eles são úteis para adicionar metadados que podem ser usados para filtrar, pesquisar e analisar spans. Por exemplo, se uma operação da aplicação onde um item é adicionado ao carrinho, você pode capturar os atributo `item_id`, `item_name`, `item_price`, `cliente_id`, etc. Essas informações podem ser usadas para analisar o comportamento do usuário, identificar problemas e muito mais.

    - Execute novamente a aplicação e acesse o endpoint [http://localhost:8080/fetch-data](http://localhost:8080/fetch-data) para gerar traces.

    - Acesse o Grafana para visualizar a telemetria gerada [http://localhost:3000](http://localhost:3000).

    Note que no Trace agora temos informações no Span Attributes.
    [Trace-Span-Attributes](./image/trace-span-attribut.png)

