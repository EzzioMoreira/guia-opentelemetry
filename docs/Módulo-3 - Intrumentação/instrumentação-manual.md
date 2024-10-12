## Instrumentação Manual

A instrumentação manual é o processo de adicionar código em aplicações para gerar dados de telemetria. A instrumentação manual é feita utilizando APIs e SDKs do OpenTelemetry.

> A instrumentação manual é recomendada para cenários em que a instrumentação sem código não é suficiente. A instrumentação sem código é recomendada quando você não tem acesso ao código da aplicação ou precisa de uma solução rápida. Nada te impede de usar os dois métodos juntos.

### Implementando Instrumentação Manual

1. Clonar o repositório e acessar o diretório do módulo:

   ```bash
    git clone https://github.com/EzzioMoreira/treinamento-opentelemetry.git
    cd treinamento-opentelemetry/docs/Modulo-2\ -\ OpenTelemetry
    ```

2. Primeiro, precisamos instalar as bibliotecas necessárias para adicionar instrumentação. Adicione os seguintes pacotes ao arquivo `requirements.txt`:

   ```txt
   opentelemetry-api
   opentelemetry-sdk
   opentelemetry-exporter-otlp
   ```

3. Para iniciar a instrumentação, é necessário instanciar o `TracerProvider`, responsável por gerenciar `Traces` e `Spans`. Diversos Spans agrupados formam um Trace. A configuração inicial também inclui a definição do `Exporter`, que envia os dados coletados (como traces) para uma solução de observabilidade.

    ```python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter

    provider = TracerProvider()
    span_exporter = OTLPSpanExporter()
    processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    ```

4. Agora, podemos adicionar spans nas funções onde desejamos rastrear o fluxo de execução. Use o trecho de código a seguir para adicionar spans na função `fetch_data_from_external_service`.

    ```python
    def fetch_data_from_external_service():
        with tracer.start_as_current_span("fetch_data_from_external_service") as span:
            # Simula uma solicitação HTTP GET para um serviço externo
            response = requests.get("http://httpbin.org/get")
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("http.url", "http://httpbin.org/get")
            span.set_attribute("http.method", "GET")
            span.add_event("Buscando dados do servico externo", {"http.status_code": response.status_code})
            sleep(latency)
            return f"GET request to httpbin.org returned {response.status_code}"
    ```

Quando definimos `start_as_current_span`, estamos criando um novo span e definindo-o como o span ativo. Isso significa que qualquer operação que ocorra dentro do bloco `with` será associada a esse span.

5. Adicione spans na funções `submit_data_to_external_service` 

    ```python
    
    ```

