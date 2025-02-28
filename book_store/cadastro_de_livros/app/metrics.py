# metrics.py
    """"
    Módulo ara configurar o MeterProvider do OpenTelemetry
    """
    # Adicione estas importações no início dos arquivos
    from opentelemetry import metrics
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import BatchExportProcessor
    from opentelemetry.exporter.otlp.metrics_exporter import OTLPMetricsExporter

    def configure_meter():
        """"
        Configura medidor com OpenTelemetry
        """
        # Configura o exportador de métricas
        exporter = OTLPMetricsExporter(
            endpoint=
        )