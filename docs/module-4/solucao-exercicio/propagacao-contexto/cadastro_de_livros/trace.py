# trace.py
"""
Módulo para configurar o rastreamento distribuído com OpenTelemetry.
"""
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def configure_tracer():
    """
    Configura o rastreamento distribuído com OpenTelemetry.
    """
    # Configura o exportador de spans
    exporter = OTLPSpanExporter(
        endpoint="http://otelcollector:4317",  # Endpoint do coletor OpenTelemetry
        insecure=True                          # Usar conexão insegura (sem TLS)
    )
    
    # Define os atributos do recurso
    resource = Resource.create({
        "service.name": "cadastro_de_livros",  # Nome do serviço
        "service.version": "0.1.0",            # Versão do serviço
        "deployment.environment": "dev"        # Ambiente de implantação
    })
    
    # Configura o TracerProvider
    provider = TracerProvider(resource=resource) # Define o recurso
    processor = BatchSpanProcessor(exporter)     # Define o exportador
    provider.add_span_processor(processor)       # Adiciona o exportador ao provider
    trace.set_tracer_provider(provider)          # Define o provider como o provider padrão
    
    # Retorna um tracer configurado
    tracer = trace.get_tracer(__name__)         # Obtém um Tracer
    return tracer                               # Retorna o Tracer
