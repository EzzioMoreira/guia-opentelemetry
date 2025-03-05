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

    # Cria o leitor para exportação periódica (ex: a cada 60s)
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)

    # Define os atributos do recurso
    resource = Resource.create({
        "service.name": "cadastro-de-livros",
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
Definição das métricas do sistema cadastrador de livros
"""
livros_cadastrados = configure_meter().create_counter(
    "bookstore.livros.cadastrados",
    description="Total de livros cadastrados",
)
