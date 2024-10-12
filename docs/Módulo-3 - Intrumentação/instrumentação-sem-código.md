## Instrumentação Sem Código

Muito conhecido como Auto-Instrumentação, é processo em que o OpenTelemetry modifica o comportamento da aplicação em tempo de execução, adicionando código para gerar, processar e enviar telemetria. Isso é possível graças a uma técnica chamada de [Monkey Patching](https://en.wikipedia.org/wiki/Monkey_patch).

> O método de aplicar instrumentação sem código pode variar de acordo com a linguagem da aplicação. 

Com isso, toda vez que uma requisição é feita na aplicação de exemplo o OpenTelemetry captura e envia essas informações para Jaeger.

## Implementando Instrumentação Sem Código

Agora, siga estes passos para executar a aplicação e visualizar os traces no Jaeger:

1. Clonar o repositório e acessar o diretório do módulo:

   ```bash
    git clone https://github.com/EzzioMoreira/treinamento-opentelemetry.git
    cd treinamento-opentelemetry/docs/Modulo-2\ -\ OpenTelemetry
    ```

1. Para implementar a instrumentação sem código, adicione o seguinte trecho de código ao arquivo `Dockerfile`:

    ```Dockerfile
    RUN pip install opentelemetry-distro opentelemetry-exporter-otlp 
    RUN opentelemetry-bootstrap -a install
    ```

    Devemos devemos instalar o [pacote distro](https://opentelemetry.io/docs/languages/python/distro/) para que a instrumentação sem código funcione corretamente, o `opentelemetry-distro` contém a distros padrões para configurar automaticamente as opções mais comuns para os usuários. O [opentelemetry-bootstrap](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/opentelemetry-instrumentation#opentelemetry-bootstrap) faz a leitura dos pacotes instalados na aplicação e instala as bibliotecas necessárias para a instrumentar a aplicação. Por exemplo, estamos utilizando o pacote `flask` na aplicação de exemplo, o `opentelemetry-bootstrap` instalará o pacote `opentelemetry-instrumentation-flask` para nós.

1. No `entrypoint` no `Dockerfile` adicione o seguinte comando:

    ```Dockerfile
    ENTRYPOINT ["opentelemetry-instrument", "python", "app.py"]
    ```

    O comando `opentelemetry-instrument` tentará detectar automaticamente os pacotes usados na aplicação e quando possível, aplicará a instrumentação. O comando suporte configurações adicionais, como a definição de um `tracer` ou `exporter` específico, veja o exemplo.

    ```shell
    opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    --service_name your-service-name \
    --exporter_otlp_endpoint 0.0.0.0:4317 \
    python myapp.py
    ```

    Como alternativa, vamos utilizar variáveis de ambiente para configurar o `opentelemetry-instrument`. Para isso, adicione o seguinte trecho de código ao arquivo `Dockerfile`:

    ```Dockerfile
    ENV OTEL_SERVICE_NAME="app-python"
    ENV OTEL_RESOURCE_ATTRIBUTES="service.version=1.0.0, env=dev"
    ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otelcollector:4317"
    ```

1. Acesse os endpoints da aplicação para gerar traces:

   - [http://localhost:8080/fetch-data](http://localhost:8080/fetch-data)
   - [http://localhost:8080/submit-data](http://localhost:8080/submit-data)
   - [http://localhost:8080/simulate-error](http://localhost:8080/simulate-error)
   
1. Acesse o Jaeger para visualizar os traces http://localhost:16686.

    Selecione o serviço `python-app` e clique em `Find Traces` para visualizar os traces gerados pelas requisições que você acabou de fazer.

### O Que Esperar?

Quando você acessar o Jaeger, verá os traces das requisições HTTP, junto com a latência e detalhes de cada requisição. Isso permitirá que você veja exatamente quanto tempo cada requisição levou e como elas fluíram pela aplicação.

![Jaeger](./images/jaeger-traces.png)

## Instrumentação Manual

A instrumentação manual é o processo de adicionar código em aplicações para gerar dados de telemetria. A instrumentação manual é feita utilizando APIs e SDKs do OpenTelemetry.

> A instrumentação manual é recomendada para cenários em que a instrumentação sem código não é suficiente. A instrumentação sem código é recomendada quando você não tem acesso ao código da aplicação ou precisa de uma solução rápida. Nada te impede de usar os dois métodos juntos.

### Implementando Instrumentação Manual

1. Primeiro, precisamos instalar as bibliotecas necessárias para adicionar instrumentação. Adicione os seguintes pacotes ao arquivo `requirements.txt`:

   ```txt
   opentelemetry-api
   opentelemetry-sdk
   opentelemetry-exporter-otlp
   ```

2. Substitua o conteúdo do `Dockerfile` pelo seguinte:
    
    ```Dockerfile
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt .
    COPY app.py .
    
    RUN pip install --no-cache-dir -r requirements.txt

    EXPOSE 8080

    CMD ["python", "app.py"]
    ```

3. Para iniciar a instrumentação, é necessário instanciar o `TracerProvider`, responsável por gerenciar `Traces` e `Spans`. Diversos Spans agrupados formam um Trace. A configuração inicial também inclui a definição do `Exporter`, que envia os dados coletados (como traces) para uma solução de observabilidade.

    ```python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter

    app = Flask(__name__)
    latency = random.randint(1, 5)

    provider = TracerProvider()
    span_exporter = OTLPSpanExporter()
    processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    ```

3. Agora, podemos adicionar spans nas funções onde desejamos rastrear o fluxo de execução. Use o trecho de código a seguir para adicionar spans na função `fetch_data_from_external_service`.

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

4. Adicione spans na funções `submit_data_to_external_service` 

    ```python
    
    ```


