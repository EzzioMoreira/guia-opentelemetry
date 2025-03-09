"""
Função principal que cria a aplicação FastAPI
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from . import models
from .logs import logger
from .databases import engine, get_db
from .trace import configure_tracer
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode

# Configura o rastreamento distribuído com OpenTelemetry
tracer = configure_tracer()

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Define a rota para criar um livro
@app.post("/livros/")
def cria_livro(request: Request, livro: models.LivroBase, db: Session = Depends(get_db)):
    """
    Rota para criar um livro
    """
    with tracer.start_as_current_span("cria_livro") as span:
        try:
            # Adiciona um novo livro no banco de dados
            logger.info(f"Criando livro: {livro}")
            novo_livro = models.cria_livro(db=db, livro=livro)

            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 201)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port  ))
            
            # Substitui o atributo titulo do livro por evento e adiciona o estoque
            span.add_event("Livro criado com sucesso", attributes={"id": novo_livro.id, "titulo": novo_livro.titulo, "estoque": novo_livro.estoque})

            logger.info(f"Livro criado com sucesso: {livro}")

            # Define o status OK ao span
            span.set_status(Status(StatusCode.OK))

            # Cria um novo span para o response
            with tracer.start_as_current_span("response") as span:
                # Instrumenta o response
                response = novo_livro
                span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 201)
                span.set_attribute(SpanAttributes.EVENT_NAME, "response")
                
                # Define status para span
                span.set_status(Status(StatusCode.OK))

                return response
        
        except Exception as e:
            logger.error(f"Erro ao criar livro: {e}")

            # Define o status Error ao span
            span.set_status(Status(StatusCode.ERROR))

            raise HTTPException(status_code=500, detail="Erro ao criar livro")
        
# Define a rota para deletar um livro pelo id
@app.delete("/livros/{id}")
def deleta_livro(request: Request, id: int, db: Session = Depends(get_db)):
    """
    Rota para deletar um livro pelo id
    """
    with tracer.start_as_current_span("deleta_livro") as span:
        try:
            # Deleta um livro no banco de dados
            logger.info(f"Deletando livro com id: {id}")
            del_livro = models.remove_livro(db, id)
            if del_livro is None:
                logger.warning(f"Livro com id {id} não encontrado")
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            logger.info(f"Livro com ID: {id} deletado com sucesso")

            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port  ))

            # Substitui o atributo titulo do livro por evento
            span.add_event("Livro deletado com sucesso", attributes={"id": del_livro.id, "titulo": del_livro.titulo})

            # Define o status OK ao span
            span.set_status(Status(StatusCode.OK))
            
            return del_livro
        
        except Exception as e:
            logger.error(f"Erro ao deletar livro: {e}")

            # Define o status Error ao span
            span.set_status(Status(StatusCode.ERROR))
            
            raise HTTPException(status_code=500, detail="Erro ao deletar livro")


# Define a rota para listar livros por id
@app.get("/livros/{id}")
def busca_livro(request: Request, id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar um livro pelo id
    """
    with tracer.start_as_current_span("busca_livro") as span:
        try:
            # Busca um livro no banco de dados
            logger.info(f"Buscando livro com id: {id}")
            livro = models.busca_livro(db, id)
            
            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port  ))
            
            # Substitui o atributo titulo do livro por evento
            span.add_event("Livro encontrado com sucesso", attributes={"id": livro.id, "titulo": livro.titulo})

            # Define o status OK ao span
            span.set_status(Status(StatusCode.OK))

            if livro is None or livro == []:
                logger.warning(f"Livro com id {id} não encontrado")
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            logger.info(f"Livro com ID: {id} encontrado com sucesso")
            
            # Cria um novo span para o response
            with tracer.start_as_current_span("response") as span:

                # Instrumenta o response
                span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 200)
                span.set_attribute(SpanAttributes.EVENT_NAME, "response")
                response = livro

                # Define status para span
                span.set_status(Status(StatusCode.OK))

                return response
        
        except Exception as e:
            logger.error(f"Erro ao buscar livro: {e}")

            # Define o status Error ao span
            span.set_status(Status(StatusCode.ERROR))

            raise HTTPException(status_code=500, detail="Erro ao buscar livro")

# Define a rota para listar todos os livros
@app.get("/livros/")
def lista_livros(request: Request, db: Session = Depends(get_db)):
    """
    Rota para listar todos os livros
    """
    with tracer.start_as_current_span("lista_todos_os_livros") as span:
        try:
            # Lista todos os livros no banco de dados
            logger.info("Listando todos os livros")
            livros = models.lista_livros(db)
            logger.info(f"{len(livros)} livros encontrados")

            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute("livros", len(livros))
            span.set_attribute(SpanAttributes.CLIENT_ADDRESS, str(request.client.host))
            span.set_attribute(SpanAttributes.CLIENT_PORT, str(request.client.port))

            # Define o status OK ao span
            span.set_status(Status(StatusCode.OK))
            
            # Cria um novo span para o response
            with tracer.start_as_current_span("response") as span:

                # Instrumenta o response
                span.set_attribute(SpanAttributes.HTTP_RESPONSE_STATUS_CODE, 200)
                span.set_attribute(SpanAttributes.EVENT_NAME, "response")
                response = livros

                # Define status para span
                span.set_status(Status(StatusCode.OK))

                return response
        
        except Exception as e:
            logger.error(f"Erro ao listar livros: {e}")

            # Define o status Error ao span
            span.set_status(Status(StatusCode.ERROR))
            
            raise HTTPException(status_code=500, detail="Erro ao listar livros")
