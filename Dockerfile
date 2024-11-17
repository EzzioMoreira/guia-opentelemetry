# Imagem base
FROM python:3.9-alpine3.20

# Instala pacotes necessários
RUN apk update && \
    apk add --no-cache sqlite-dev

# Configura o diretório de trabalho
WORKDIR /app

# Copia apenas o arquivo requirements.txt primeiro para instalar dependências
COPY ./app-python/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY ./app-python/ .

# Instala OpenTelemetry e inicializa bootstrap
RUN pip install opentelemetry-distro opentelemetry-exporter-otlp && \
    opentelemetry-bootstrap -a install

# Executa o script para criar o banco de dados SQLite
RUN python create_db.py

# Expõe a porta 8080
EXPOSE 8080

# ENTRYPOINT para iniciar com o OpenTelemetry
ENTRYPOINT ["opentelemetry-instrument", "python", "app.py"]
