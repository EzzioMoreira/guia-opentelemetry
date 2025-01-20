# Imagem base
FROM python:3.12-slim

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instale-as 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o contêiner 
COPY . .

#####################################################################################
#### Adicione na linha abaixo o comando para instalar o OpenTelemetry SDK Python ####

# Expõe a porta 8082
EXPOSE 8082

#####################################################################################
#### Adicione na linha abaixo o comando para iniciar o OpenTelemetry SDK Python ####
ENTRYPOINT ["python", "-m", "app.main"]
