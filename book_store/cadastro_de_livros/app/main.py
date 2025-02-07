"""
Função principal que cria a aplicação FastAPI
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from . import models
from . import logger
from .databases import engine, get_db
from .trace import configure_tracer
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.semconv.trace import SpanAttributes

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Configura o rastreamento distribuído com OpenTelemetry
tracer = configure_tracer()

# Instrumenta o Flask para rastreamento distribuído
FastAPIInstrumentor.instrument_app(app)

# Define a rota para criar um livro
@app.post("/livros/")
def cria_livro(request: Request, livro: models.LivroBase, db: Session = Depends(get_db)):
    """
    Rota para criar um livro
    """
    with tracer.start_as_current_span("criar_livro") as span:
        try:
            logger.info(f"Criando livro: {livro}")
            novo_livro = models.cria_livro(db=db, livro=livro)
            
            # Adiciona atributos semânticos e personalizados ao span
            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 201)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute("livro.id", novo_livro.id)
            span.set_attribute("livro.titulo", novo_livro.titulo)
            
            logger.info(f"Livro criado com sucesso: {livro}")
            
            return novo_livro       
        
        except Exception as e:
            logger.error(f"Erro ao criar livro: {e}")
            raise HTTPException(status_code=500, detail="Erro ao criar livro")

# Define a rota para listar livros por id
@app.get("/livros/{id}")
def busca_livro(request: Request, id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar um livro pelo id
    """
    with tracer.start_as_current_span("buscar_livro_por_id") as span:
        try:
            logger.info(f"Buscando livro com id: {id}")
            livro = models.busca_livro(db, id)

            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute("livro.titulo", livro.titulo)
            
            if livro is None:
                logger.warning(f"Livro com id {id} não encontrado")
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            logger.info(f"Livro com ID: {id} encontrado com sucesso")
            return livro
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar livro: {e} ou livro não encontrado")
            raise HTTPException(status_code=500, detail="Erro ao buscar livro")

# Define a rota para listar todos os livros
@app.get("/livros/")
def lista_livros(request: Request, db: Session = Depends(get_db)):
    """
    Rota para listar todos os livros
    """
    with tracer.start_as_current_span("listar_todos_os_livros") as span:
        try:
            logger.info("Listando todos os livros")
            livros = models.lista_livros(db)

            span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
            span.set_attribute(SpanAttributes.HTTP_URL, str(request.url))
            span.set_attribute("livros", len(livros))

            logger.info(f"{len(livros)} livros encontrados")
            
            return livros
        
        except Exception as e:
            logger.error(f"Erro ao listar livros: {e}")
            raise HTTPException(status_code=500, detail="Erro ao listar livros")
