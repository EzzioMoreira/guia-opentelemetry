## Instrumentação Sem Código

Também conhecido como Auto-Instrumentação, é processo em que o OpenTelemetry modifica o comportamento da aplicação em tempo de execução, adicionando código para gerar, processar e enviar telemetria. Isso é possível graças a uma técnica chamada de [Monkey Patching](https://en.wikipedia.org/wiki/Monkey_patch).

> O método de aplicar instrumentação sem código varia de acordo com a linguagem de programação. 

Com isso, toda vez que uma requisição é feita na aplicação de exemplo o OpenTelemetry captura e envia a telemetria para OpenTelemetry Collector, que por sua vez, envia para o Grafana.

Instrumentação sem código é um bom começo para iniciar sua jornada com instrumentação de aplicações, mas é importante lembrar que a instrumentação sem código não é suficiente para todos os cenários. Em alguns casos, você precisará adicionar código manualmente para instrumentar corretamente a aplicação.

## Implementando Instrumentação Sem Código

Agora, siga estes passos para implementar a instrumentação sem código na aplicação Python de exemplo:

1. Clonar o repositório e acessar o diretório do módulo:

   ```bash
    git clone https://github.com/EzzioMoreira/treinamento-opentelemetry.git
    cd treinamento-opentelemetry/docs/Módulo-3\ -\ Instrumentação
    ```

1. Para implementar a instrumentação sem código, adicione o seguinte trecho de código ao arquivo `Dockerfile`:

    ```Dockerfile
    RUN pip install opentelemetry-distro opentelemetry-exporter-otlp 
    RUN opentelemetry-bootstrap -a install
    ```

    Devemos instalar o [pacote distro](https://opentelemetry.io/docs/languages/python/distro/) para que a instrumentação sem código funcione corretamente, o `opentelemetry-distro` contém a distros padrões para configurar automaticamente as opções mais comuns para os usuários. O [opentelemetry-bootstrap](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/opentelemetry-instrumentation#opentelemetry-bootstrap) faz a leitura dos pacotes instalados na aplicação e instala as bibliotecas necessárias para instrumentar a aplicação. Por exemplo, estamos utilizando o pacote `Flask` na aplicação de exemplo, o `opentelemetry-bootstrap` instalará o pacote `opentelemetry-instrumentation-flask` para nós.

1. No `entrypoint` no `Dockerfile` adicione o seguinte comando:

    ```Dockerfile
    ENTRYPOINT ["opentelemetry-instrument", "python", "app.py"]
    ```

    O comando `opentelemetry-instrument` tentará detectar automaticamente os pacotes usados na aplicação e quando possível, aplicará a instrumentação. O comando suporta configurações adicionais, como a definição de um `tracer` ou `exporter` específico, veja o exemplo.

    ```shell
    opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    --service_name your-service-name \
    --exporter_otlp_endpoint 0.0.0.0:4317 \
    python myapp.py
    ```

    Como alternativa, vamos utilizar variáveis de ambiente para configurar o `opentelemetry-instrument`. Para isso, adicione o seguinte trecho de código ao arquivo `docker-compose.yaml`:

    ```yaml
    environment:
      - OTEL_SERVICE_NAME=app-python
      - OTEL_RESOURCE_ATTRIBUTES=service.name=app-python, service.version=1.0.0, service.env=dev
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otelcollector:4317
      - OTEL_EXPORTER_OTLP_INSECURE=true
      - OTEL_PYTHON_LOG_CORRELATION=true
    ```

1. Pronto! Agora, basta executar o comando `docker-compose up` para iniciar a aplicação.

    ```shell
    docker-compose up
    ```

1. Acesse os endpoints da aplicação para gerar métricas e traces:

   - [http://localhost:8080/fetch-data](http://localhost:8080/fetch-data)
   - [http://localhost:8080/submit-data](http://localhost:8080/submit-data)
   - [http://localhost:8080/simulate-error](http://localhost:8080/simulate-error)
   
1. Acesse o Grafana para visualizar a telemetria gerada http://localhost:3000.

    No menu `explorer` do Grafana, você pode visualizar as métricas e traces, selecione `service.name` = `app-python` para visualizar as métricas e traces.

### O Que Esperar?

Quando você acessar os endpoints da aplicação, o OpenTelemetry irá capturar as requisições e enviar para o OpenTelemetry Collector. O OpenTelemetry Collector irá processar e enviar a telemetria para Tempo, Mimir e Loki. Por fim, você poderá visualizar a telemetria no Grafana.

## Conclusão

Neste módulo, você aprendeu como implementar a instrumentação sem código em uma aplicação Python. A instrumentação sem código é uma maneira fácil e rápida de adicionar telemetria em aplicações sem a necessidade de alterar o código fonte.

## Saiba Mais

- [OpenTelemetry Python](https://opentelemetry.io/docs/zero-code/)
- [Byte Buddy](https://bytebuddy.net/#/)
