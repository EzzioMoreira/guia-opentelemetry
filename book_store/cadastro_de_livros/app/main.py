"""
Função principal que cria a aplicação FastAPI
"""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models
from . import logger
from .databases import engine, get_db

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Define a rota para criar um livro
@app.post("/livros/")
def cria_livro(livro: models.LivroBase, db: Session = Depends(get_db)):
    """
    Rota para criar um livro
    """
    try:
        logger.info(f"Criando livro: {livro}")
        novo_livro = models.cria_livro(db=db, livro=livro)
        logger.info(f"Livro criado com sucesso: {livro}")
        return novo_livro
    except Exception as e:
        logger.error(f"Erro ao criar livro: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar livro")

# Define a rota para listar livros por id
@app.get("/livros/{id}")
def busca_livro(id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar um livro pelo id
    """
    try:
        logger.info(f"Buscando livro com id: {id}")
        livro = models.busca_livro(db, id)
        if livro is None:
            logger.warning(f"Livro com id {id} não encontrado")
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        logger.info(f"Livro com ID: {id} encontrado com sucesso")
        return livro
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar livro: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar livro")

# Define a rota para listar todos os livros
@app.get("/livros/")
def lista_livros(db: Session = Depends(get_db)):
    """
    Rota para listar todos os livros
    """
    try:
        logger.info("Listando todos os livros")
        livros = models.lista_livros(db)
        logger.info(f"{len(livros)} livros encontrados")
        return livros
    except Exception as e:
        logger.error(f"Erro ao listar livros: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar livros")
