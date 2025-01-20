"""
Modulo responsável por manipular os dados do banco de dados
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .databases import Base
from . import logger

# Define o atributo comum a todas as classes
class OrdemBase(BaseModel):
    id_livro: int
    
# Classe que herda os atributos da classe OrdemBase e adiciona os campos id e status
class OrdemCreate(OrdemBase):
    pass

# Classe que representa a entidade completa de uma Ordem
class Ordem(OrdemBase):
    id: int # Identificação da ordem
    status: str # Status da ordem (ex. Pendente, Aprovado, Cancelado)
    
    class Config:
        from_attributes = True # Permite que a classe seja compatível com objetos ORM (Object Relational Mapping)

# Define a classe OrdemDB contendo os campos para criação da tabela no banco de dados
class OrdemDB(Base):
    __tablename__ = "ordens" # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True) # Campo de identificação da ordem
    id_livro = Column(Integer) # Campo de identificação do livro
    status = Column(String) # Campo de status da ordem

# Função que cria uma ordem no banco de dados
def cria_ordem(db: Session, ordem: OrdemCreate):
    """
    Função que cria uma ordem no banco de dados
    """
    db_ordem = OrdemDB(
        id_livro=ordem.id_livro,
        status="Pendente"
    )
    db.add(db_ordem)
    db.commit()
    db.refresh(db_ordem)
    return db_ordem

# Função que retorna ordem do banco de dados
def lista_ordem(db: Session, id_ordem: int):
    """
    Função que retorna uma ordem do banco de dados
    """
    try:
        return db.query(OrdemDB).filter(OrdemDB.id == id_ordem).first()
    except Exception as e:
        logger.error(f"Erro ao buscar ordem com id {id_ordem}: {e}")
        raise
