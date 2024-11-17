# Imagem base
FROM python:3.9-alpine3.20

# Instala pacotes necessários
RUN apk update &&\
    apk add --no-cache sqlite-dev

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e fonte
COPY ./app-python/. .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instala OpenTelemetry e Gunicorn (se necessário)
# Instala OpenTelemetry e Gunicorn (se necessário)
RUN pip install opentelemetry-distro opentelemetry-exporter-otlp &&\
    opentelemetry-bootstrap -a install
``
RUN opentelemetry-bootstrap -a install

# Executa o script para criar o banco de dados SQLite
RUN python create_db.py

# Expõe a porta 8080
EXPOSE 8080

# ENTRYPOINT para iniciar o Gunicorn com OpenTelemetry
ENTRYPOINT ["opentelemetry-instrument", "python", "app.py"]
