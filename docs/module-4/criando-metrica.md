## Criando Métricas

Antes de começar a criar métricas do sistema Bookstore, precisamos entender quais são os tipos de instrumentos do OpenTelemetry:

- **Counter**: Um valor que acumula com o tempo, esse valor só cresce ou pode ser redefinido para zero na reinicialização. São muito utilizadas para contagem de eventos: número de requisições HTTP, número de erros, quantidade de acessos. 

- **Gauge**: Um valor que pode aumentar ou diminuir ao longo do tempo. São muito utilizadas para representar valores instantâneos: uso de CPU, memória, etc.

- **Histogram**: Um contador que fornece a distribuição de valores em um intervalo. São muito utilizadas para medir a distribuição de valores: tempo de resposta de uma requisição entre 0-100ms, 100-200ms, tamanho de arquivos.

### Cardinalidade

Cardinalidade se refere ao número de valores possíveis que uma métrica pode assumir. Métricas com alta cardinalidade podem ser mais difíceis de armazenar e processar.

Muitos sistemas de banco de dados não conseguem lidar com eficiência com o volume de dados gerado por métricas de alta cardinalidade. Por isso, é importante entender a cardinalidade dos dados que você está gerando, coletando e armazenando.

**Alta Cardinalidade**: "Monitorar os números de placa de cada carro no estacionamento." (Muitos valores únicos, um para cada carro).

**Baixa Cardinalidade**: "Contar quantos carros são de cada cor no estacionamento." (Poucos valores únicos, como vermelho, azul, preto).

### Instrumentando o código

1. Para criar métricas no OpenTelemetry, você precisa de um `Meter` que é responsável por criar e gerenciar métricas. Vamos iniciar a criação das métricas no serviço de Cadastro de Livros. Para deixar a estrutura do projeto mais organizado, crie um arquivo chamado `metrics.py` no diretório Cadastro de Livros. 
    
    Crie um arquivo chamado `metrics.py` no diretório `app` da aplicação Cadastro de Livros.

    ```python
    # metrics.py
    """"
    Módulo ara configurar o MeterProvider do OpenTelemetry
    """
    # Adicione estas importações no início dos arquivos
    from opentelemetry import metrics
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import BatchExportProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    def configure_meter():
        """"
        Configura medidor com OpenTelemetry
        """
        # Configura o exportador de métricas
        exporter = OTL
    ```



