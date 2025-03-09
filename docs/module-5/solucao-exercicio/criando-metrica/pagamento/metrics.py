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
        "service.name": "pagamento",
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

duracao_pagamento = configure_meter().create_histogram(
    name="bookstore.duracao.pagamento",
    description="Duração do pagamento",
    unit="ms",
)

tamanho_pool = configure_meter().create_gauge(
    name="database.pool.size",
    description="Tamanho total da pool de conexões",
    unit="1",
)
