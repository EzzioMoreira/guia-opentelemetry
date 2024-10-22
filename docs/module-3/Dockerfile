# Imagem base
FROM python:3.9-slim

# Configura o diretório de trabalho
WORKDIR /app

# Copia o requirements.txt para o container
COPY requirements.txt .

# Copia o código fonte para o container
COPY app.py .

# Instala as dependências, incluindo OpenTelemetry e a instrumentação para Flask
RUN pip install --no-cache-dir -r requirements.txt

####################################################################
#### Adicione aqui o comando RUN para instalar o OpenTelemetry #####
####################################################################

# Expõe a porta 8080
EXPOSE 8080
######################################################################
# Altere o entrypoint para executar o OpenTelemetry Instrumentation ##
ENTRYPOINT ["python", "app.py"]
######################################################################
