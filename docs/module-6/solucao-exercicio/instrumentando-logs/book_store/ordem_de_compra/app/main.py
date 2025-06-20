"""
Função principal que cria a aplicação FastAPI
"""
import os
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import requests
from . import models
from .databases import engine, get_db
from .logs import logger
from .trace import configure_tracer
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode
from .metrics import duracao_ordem
import time

# Configura o rastreamento distribuído com OpenTelemetry
tracer = configure_tracer()

# Obtém url dos serviços pagamento e cadastro de livros
PAYMENT_URL = os.getenv("PAYMENT_URL", "http://pagamento:8082")
BOOK_URL = os.getenv("BOOK_URL", "http://cadastro_de_livros:8080")

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Define a rota para criar uma ordem
@app.post("/ordens/", response_model=models.Ordem)
def cria_ordem(request: Request, ordem: models.OrdemCreate, db: Session = Depends(get_db)):
    """
    Rota para criar uma ordem de compra de um livro
    """
    with tracer.start_as_current_span("cria_ordem") as span:
        try:
            # Inicia o contado de tempo
            start_time = time.time()

            # Valida disponibilidade do livro no serviço de cadastro de livros
            livro_response = requests.get(f"{BOOK_URL}/livros/{ordem.id_livro}")
            if livro_response.status_code != 200:
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            
            # Valida se o livro está disponível em estoque
            livro = livro_response.json()
            if livro["estoque"] <= 0:
                raise HTTPException(status_code=404, detail="Livro esgotado")
            
            # Cria ordem de compra
            db_ordem = models.cria_ordem(db=db, ordem=ordem)
            
            # Enviar pagamento para o serviço de Pagamento 
            pagamento_response = requests.post(f"{PAYMENT_URL}/pagamentos", json={"id_ordem": db_ordem.id}) 
            if pagamento_response.status_code != 200: 
                raise HTTPException(status_code=400, detail="Falha no processamento do pagamento")
            pagamento_response = pagamento_response.json()
            
            # Atualiza status da ordem
            if pagamento_response["status"] == "Aprovado":
                db_ordem.status = "Concluído"
            else:
                db_ordem.status = "Pagamento Recusado"
        
            db.commit()
            db.refresh(db_ordem)

            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 201)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port))

            # Substitui o atributo da ordem por evento
            span.add_event("Ordem criada com sucesso", attributes={"id_ordem": db_ordem.id, "id_livro": db_ordem.id_livro, "status": db_ordem.status})

            # Define o status OK ao span
            span.set_status(Status(StatusCode.OK))
            
            # Cria um novo span para o response
            with tracer.start_as_current_span("response") as span:
                # Instrumenta o response
                response = db_ordem
                span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 201)
                span.set_attribute(SpanAttributes.EVENT_NAME, "response")
                
                # Define status para span
                span.set_status(Status(StatusCode.OK))

                # Calcula a duração da ordem em milissegundos
                duracao = (time.time() - start_time) * 1000
                # Registra a duração da ordem
                duracao_ordem.record(duracao, {"status": db_ordem.status})

                return response

        except Exception as e:
            logger.error(f"Erro ao criar ordem: {str(e)}")

            # Define o status Error ao span
            span.set_status(Status(StatusCode.ERROR))

            raise HTTPException(status_code=500, detail=f"Erro ao criar ordem {str(e)}")

# Define a rota para listar ordens por id
@app.get("/ordens/{id}", response_model=models.Ordem)
def busca_ordem(request: Request, id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar uma ordem pelo id
    """
    with tracer.start_as_current_span("busca_ordem") as span:
        try:
            logger.info(f"Buscando ordem com id: {id}")
            ordem = models.lista_ordem(db=db, id_ordem=id)
            if ordem is None:
                logger.warning(f"Ordem com id {id} não encontrada")
                raise HTTPException(status_code=404, detail="Ordem não encontrada")
            
            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port))
            
            # Substitui o atributo da ordem por evento
            span.add_event("Ordem encontrada com sucesso", attributes={"id": ordem.id, "id_livro": ordem.id_livro, "status": ordem.status})

            # Define o status OK ao span
            span.set_status(Status(StatusCode.OK))

            # Cria um novo span para o response
            with tracer.start_as_current_span("response") as span:
                # Instrumenta o response
                response = ordem
                span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 200)
                span.set_attribute(SpanAttributes.EVENT_NAME, "response")
                
                # Define status para span
                span.set_status(Status(StatusCode.OK))

                return response

        except Exception as e:
            logger.error(f"Erro ao buscar ordem: {e}")

            # Define o status Error ao span
            span.set_status(Status(StatusCode.ERROR))

            raise HTTPException(status_code=500, detail="Erro ao buscar ordem")
