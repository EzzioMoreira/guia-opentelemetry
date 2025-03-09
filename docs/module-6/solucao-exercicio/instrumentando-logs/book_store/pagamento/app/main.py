from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import random
import requests
import os
from . import models
from .databases import engine, get_db
from .logs import logger
from .trace import configure_tracer
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode
from .metrics import duracao_pagamento
import time

# Configura o rastreamento distribuído com OpenTelemetry
tracer = configure_tracer()

# Obtém url dos serviços ordem de compra
ORDER_URL = os.getenv("ORDER_URL", "http://ordem_de_compra:8081")

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Define a rota para processar pagamento
@app.post("/pagamentos", response_model=models.Pagamento)
def processar_pagamento(request: Request, pagamento: models.PagamentoCreate, db: Session = Depends(get_db)):
    """
    Processa um pagamento para a ordem especificada
    """
    with tracer.start_as_current_span("processar_pagamento") as span:
        try:
            # Inicia o contador de tempo
            start_time = time.time()

            # Valida se a ordem de compra existe
            ordem_response = requests.get(f"{ORDER_URL}/ordens/{pagamento.id_ordem}")
            if ordem_response.status_code != 200:

                # Adiciona atributos semânticos e personalizados ao span
                span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
                span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 404)
                span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
                span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
                span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port))
                
                # Substitui o atributo sobre a ordem de compra por evento
                span.add_event("Ordem de compra não encontrada", attributes={"ordem.id": pagamento.id_ordem})
                
                # Define o status de Erro ao span
                span.set_status(Status(StatusCode.ERROR))
                raise HTTPException(status_code=404, detail="Ordem de compra não encontrada")
            
            # Processa pagamento
            status = random.choice(["Aprovado", "Recusado"])

            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 201)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port))

            # Substitui o atributo sobre o pagamento por evento
            span.add_event("Pagamento processado com sucesso", attributes={"pagamento.status": status})
            
            # Cria o pagamento no banco
            db_pagamento = models.processar_pagamento(db=db, pagamento=pagamento, status=status)
            
            # Definição o status OK ao span
            span.set_status(Status(StatusCode.OK))

            with tracer.start_as_current_span("response") as span:
                # Instrumenta o response
                response = db_pagamento
                span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 201)
                span.set_attribute(SpanAttributes.EVENT_NAME, "response")
                
                # Define status para span
                span.set_status(Status(StatusCode.OK))

                # Calcula a duração do pagamento em milissegundos
                duracao = (time.time() - start_time ) * 1000
                # Registra a duração do pagamento
                duracao_pagamento.record(duracao, {"status": status})

                return response
        except Exception as e:
            logger.error(f"Erro ao processar pagamento: {str(e)}")

            # Define o status de Erro ao span
            span.set_status(Status(StatusCode.ERROR))

            raise HTTPException(status_code=500, detail=f"Erro ao processar pagamento: {str(e)}")

@app.get("/pagamentos/{id_pagamento}", response_model=models.Pagamento)
def lista_pagamentos(request: Request, id_pagamento: int, db: Session = Depends(get_db)):
    """
    Retorna informações de um pagamento pelo ID
    """
    with tracer.start_as_current_span("lista_pagamentos") as span:    
        db_pagamento = models.lista_pagamentos(db=db, id_pagamento=id_pagamento)

        # Adiciona atributos semânticos e personalizados ao span
        span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
        span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
        span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
        span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port))

        # Substitui o atributo sobre o pagamento por evento
        span.add_event("Pagamento listado com sucesso", attributes={"pagamento.id": id_pagamento})

        # Define o status OK ao span
        span.set_status(Status(StatusCode.OK))

        if db_pagamento is None:
            # Define o status de Erro ao span
            span.set_status(Status(StatusCode.ERROR))

            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        with tracer.start_as_current_span("response") as span:
            # Instrumenta o response
            response = db_pagamento
            span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.EVENT_NAME, "response")
            
            # Define status para span
            span.set_status(Status(StatusCode.OK))

            return response
