# Imagem base
FROM python:3.9-slim

# Configura o diretório de trabalho
WORKDIR /app

# Copie os arquivos de dependências e instale-as 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o contêiner 
COPY . .

#####################################################################################
#### Adicione na linha abaixo o comando para instalar o OpenTelemetry SDK Python ####

# Expõe a porta 8080
EXPOSE 8080

#####################################################################################
#### Adicione na linha abaixo o comando para iniciar o OpenTelemetry SDK Python ####
ENTRYPOINT ["python", "-m", "app.main"]
