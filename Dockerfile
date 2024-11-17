# Imagem base
FROM python:3.9-slim

# Instala pacotes necessários
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev

# Configura o diretório de trabalho
WORKDIR /app

# Copia apenas o arquivo requirements.txt primeiro para instalar dependências
COPY ./app-python/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY ./app-python/ .

#####################################################################################
#### Adicione na linha abaixo o comando para instalar o OpenTelemetry SDK Python ####

# Executa o script para criar o banco de dados SQLite
RUN python create_db.py

# Expõe a porta 8080
EXPOSE 8080

#####################################################################################
#### Adicione na linha abaixo o comando para iniciar o OpenTelemetry SDK Python ####
ENTRYPOINT ["python", "app.py"]
