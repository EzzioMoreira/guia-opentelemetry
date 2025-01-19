"""
Modulo responsável por manipular os dados do banco de dados
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .databases import Base

# Define a classe OrdemBase contendo os campos id_livro para serem usados na criação de uma ordem
class OrdemBase(BaseModel):
    id_livro: int
    
# Define a classe OrdemCreate contendo os campos id_livro para serem usados na criação de uma ordem
class OrdemCreate(OrdemBase):
    pass

# Define a classe Ordem incluindo os campos id, status para serem usados na criação de uma ordem
class Ordem(OrdemBase):
    id: int # Identificação da ordem
    status: str # Status da ordem (ex. Pendente, Aprovado, Cancelado)
    
    class Config:
        from_attributes = True # Configuração para permitir a leitura de objetos ORM

# Define a classe OrdemDB contendo os campos para criação da tabela no banco de dados
class OrdemDB(Base):
    __tablename__ = "ordens" # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True) # Campo de identificação da ordem
    id_livro = Column(Integer) # Campo de identificação do livro
    status = Column(String) # Campo de status da ordem

# Função para criar uma ordem
def cria_ordem(db: Session, ordem: OrdemCreate):
    db_ordem = OrdemDB(
        id_livro=ordem.id_livro,
        status="Pendente"
    )
    db.add(db_ordem)
    db.commit()
    db.refresh(db_ordem)
    return db_ordem

# Função para listar uma ordem
def lista_ordem(db: Session, ordem_id: int):
    return db.query(OrdemDB).filter(OrdemDB.id == ordem_id).first()
