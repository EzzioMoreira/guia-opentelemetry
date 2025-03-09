"""
Módulo para configurar o LoggerProvider do OpenTelemetry
"""
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

# Configura o exportador de logs (mesmo endpoint do coletor)
exporter = OTLPLogExporter(
    endpoint="http://otelcollector:4318/v1/logs"
)

# Configura recursos (mesmo usado nas métricas/traces)
resource = Resource.create({
    "service.name": "ordem-de-compra",
    "service.version": "0.1.0",
    "deployment.environment": "dev",
})

# Configura o LoggerProvider
provider = LoggerProvider(resource=resource)
provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
set_logger_provider(provider)

# Configura o handler OpenTelemetry para logging padrão
handler = LoggingHandler(logger_provider=provider)
logging.basicConfig(handlers=[handler], level=logging.INFO, force=True)

# Cria o logger global
logger = logging.getLogger(__name__)
