# Etapa de build (usando Gradle)
FROM gradle:7.6.2-jdk17 AS build

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY ./gs-spring-boot/complete .

# Compila o projeto e gera o JAR
RUN ./gradlew bootJar

# Etapa final (runtime) com autoinstrumentação OpenTelemetry
FROM eclipse-temurin:17-jre

# Configura o diretório de trabalho
WORKDIR /app

# Baixa o agente OpenTelemetry
RUN curl -L -o opentelemetry-javaagent.jar https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar

# Copia o JAR gerado na etapa de build
COPY --from=build /app/build/libs/*.jar app.jar

# Exponha a porta padrão do Spring Boot
EXPOSE 8080

# Configura variáveis de ambiente para o OpenTelemetry (somente no runtime)
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar"

# Comando para executar a aplicação
ENTRYPOINT ["java", "-jar", "app.jar"]
