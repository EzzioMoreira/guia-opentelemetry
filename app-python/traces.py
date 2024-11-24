"""
Modulo para configurar o rastreamento de spans com OpenTelemetry.
"""
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource


def setup_tracing():
    """
    Configura e retorna o TracerProvider para rastreamento.
    """
    # Obtém atributos de recurso da variável de ambiente ou define padrões
    resource_attributes = os.environ.get("OTEL_RESOURCE_ATTRIBUTES") or "service.name=app-python,service.version=0.1.0,service.env=dev"
    key_value_pairs = resource_attributes.split(',')
    result_dict = {}

    # Converte atributos no formato chave=valor para um dicionário
    for pair in key_value_pairs:
        key, value = pair.split('=')
        result_dict[key.strip()] = value.strip()

    # Define atributos de recurso
    resource_attributes = {
        "service.name": result_dict.get("service.name", "app-python"),
        "service.version": result_dict.get("service.version", "0.1.0"),
        "service.env": result_dict.get("service.env", "dev")
    }

    resource = Resource.create(resource_attributes)

    # Configura o exportador OTLP
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(insecure=True))
    provider.add_span_processor(processor)

    # Registra o TracerProvider como padrão
    trace.set_tracer_provider(provider)

    # Retorna um tracer configurado
    return trace.get_tracer(__name__)


# Configura e cria o tracer ao importar o módulo
tracer = setup_tracing()
