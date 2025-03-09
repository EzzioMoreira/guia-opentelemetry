# metrics.py
"""
Módulo para configurar o MeterProvider do OpenTelemetry
"""
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader  # Importante!
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

def configure_meter():
    """
    Configura medidor com OpenTelemetry.
    """
    # Configura o exportador de métricas (correção da porta)
    exporter = OTLPMetricExporter(
        endpoint="http://otelcollector:4318/v1/metrics",               
    )

    # Cria o leitor para exportação periódica (ex: a cada 10 segundos)
    reader = PeriodicExportingMetricReader(exporter)

    # Define os atributos do recurso
    resource = Resource.create({
        "service.name": "ordem-de-compra",
        "service.version": "1.0.0",
        "deployment.environment": "dev",
    })

    # Cria o provedor de métricas com o leitor
    provider = MeterProvider(
        resource=resource,
        metric_readers=[reader]  # Adiciona o leitor ao provider
    )
    metrics.set_meter_provider(provider)

    # Retorna o medidor para criar métricas
    return metrics.get_meter(__name__)

"""
Definição das métricas do sistema de pagamento
"""

# Cria a métrica para contar a quantidade de ordens de compra
ordem_compra = configure_meter().create_counter(
    name="bookstore.orden.compra",
    description="Quantidade de ordens de compra",
    unit="number",
)

# Cria a métrica para medir o tempo de processamento de uma ordem de compra
duracao_ordem = configure_meter().create_histogram(
    name="bookstore.duracao.ordem",
    description="Tempo de processamento de uma ordem de compra",
    unit="ms"
)
