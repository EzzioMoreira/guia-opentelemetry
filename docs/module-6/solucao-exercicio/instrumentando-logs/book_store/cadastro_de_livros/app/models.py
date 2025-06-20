"""
Modulo responsável por manipular os dados do banco de dados
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .databases import Base
from .logs import logger
from .metrics import livros_cadastrados, estoque_livros

# Modelo Pydantic para para entrada livre de dados
class LivroBase(BaseModel):
    titulo: str
    estoque: int
    
    class Config:
        from_attributes = True

# Define a classe Book que representa a tabela de livros no banco de dados
class Livros(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    estoque = Column(Integer)

# Função que cria um livro no banco de dados
def cria_livro(db: Session, livro: LivroBase):
    """
    Função que cria um livro no banco de dados
    """
    try:
        db_livro = Livros(titulo=livro.titulo, estoque=livro.estoque)
        db.add(db_livro)
        db.commit()
        db.refresh(db_livro)

        # Incrementa a métrica total_livros_cadastrados
        livros_cadastrados.add(1)

        # Atualiza a métrica estoque_livros
        estoque_livros.set(db.query(Livros).count())
        
        return db_livro
    except Exception as e:
        logger.error(f"Erro ao criar livro no banco de dados: {e}")
        raise

# Função que remove um livro do banco de dados
def remove_livro(db: Session, livro_id: int):
    """
    Função que remove um livro do banco de dados
    """
    try:
        db_livro = db.query(Livros).filter(Livros.id == livro_id).first()
        if db_livro:
            db.delete(db_livro)
            db.commit()
            
            # Atualiza a métrica estoque_livros
            estoque_livros.set(db.query(Livros).count())
            
            return db_livro
    except Exception as e:
        logger.error(f"Erro ao remover livro do banco de dados: {e}")
        raise

# Função que retorna todos os livros do banco de dados
def lista_livros(db: Session):
    """
    Função que retorna todos os livros do banco de dados
    """
    try:
        return db.query(Livros).all()
    except Exception as e:
        logger.error(f"Erro ao listar livros: {e}")
        raise

# Função que retorna um livro do banco de dados
def busca_livro(db: Session, livro_id: int):
    """
    Função que retorna um livro do banco de dados
    """
    try:
        return db.query(Livros).filter(Livros.id == livro_id).first()
    except Exception as e:
        logger.error(f"Erro ao buscar livro com id {livro_id}: {e}")
        raise
