"""
Modulo para configurar o rastreamento de spans com OpenTelemetry.
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource


def setup_tracing():
    """
    Configura e retorna o TracerProvider para rastreamento.
    """
    resource_attributes = os.environ.get("OTEL_RESOURCE_ATTRIBUTES") or 'service.name=app-python,service.version=0.1.0,service.env=dev'
    key_value_pairs = resource_attributes.split(',')
    result_dict[Key] = value
    
    for pair in key_value_pairs:
        key, value = pair.split('=')
        result_dict[key] = value
    
    resourceAttributes = {
        "service.name": otel_service_name,
        "service.version": result_dict['otel_service_version'],
        "service.env": result_dict['otel_service_env']
    }
    
    resource = Resource.create(resourceAttributes)

    # Configura o exportador OTLP para enviar os spans para o OpenTelemetry Collector
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    
    # Registra o TracerProvider como o provedor de rastreamento padrão
    trace.set_tracer_provider(provider)
    
    # Cria um tracer com o nome do módulo
    tracer = trace.get_tracer(otel_service_name)
    return tracer
