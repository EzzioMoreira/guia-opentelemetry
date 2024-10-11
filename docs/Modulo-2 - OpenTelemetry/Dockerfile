# Imagem base
FROM python:3.9-slim

# Configura o diretório de trabalho
WORKDIR /app

# Copia o requirements.txt para o container
COPY requirements.txt .

# Instala as dependências, incluindo OpenTelemetry e a instrumentação para Flask
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install opentelemetry-distro opentelemetry-exporter-otlp

RUN opentelemetry-bootstrap -a install
# Copia o código fonte para o container
COPY app.py .

# Expõe a porta 8080
EXPOSE 8080

# Configura a autoinstrumentação e executa o app.py
CMD ["opentelemetry-instrument", "python", "app.py"]
