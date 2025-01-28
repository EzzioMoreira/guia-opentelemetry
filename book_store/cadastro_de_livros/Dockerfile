# Imagem base
FROM python:3.12-slim

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instale-as 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o contêiner 
COPY . .

########################################################################################################
#### Adicione na linha abaixo o comando para instalar os pacotes necessário do OpenTelemetry Python ####
#RUN pip install -I "opentelemetry-distro=0.43b0" "opentelemetry-exporter-otlp=0.43b0" && \
RUN opentelemetry-bootstrap -a install

# Expõe a porta
EXPOSE 8080

########################################################################################
#### Adicione na linha abaixo o opentelemetry-instrument para instrumentar o código ####
CMD ["opentelemetry-instrument", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
