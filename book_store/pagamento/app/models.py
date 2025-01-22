from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .databases import Base

# Define a classe PagamentoBase
class PagamentoBase(BaseModel):
    id_ordem: int

# Define a classe PagamentoCreate
class PagamentoCreate(PagamentoBase):
    pass

# Define a classe Pagamento
class Pagamento(PagamentoBase):
    id: int
    status: str

    class Config:
        from_attributes = True

# Define a classe Pagamento
class PagamentoDB(Base):
    __tablename__ = 'pagamentos'
    id = Column(Integer, primary_key=True, index=True)
    id_ordem = Column(Integer, index=True)
    status = Column(String)

# Função que processa o pagamento de uma ordem
def processar_pagamento(db: Session, pagamento: PagamentoCreate, status: str):
    """"
    Função que cria um pagamento no banco de dados
    """
    db_pagamento = PagamentoDB(
        id_ordem=pagamento.id_ordem,
        status=status
    )
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento

# Função que lista os pagamento
def lista_pagamentos(db: Session, id_pagamento: int):
    """"
    Função que retorna um pagamento do banco de dados
    """
    try:
        return db.query(PagamentoDB).filter(PagamentoDB.id == id_pagamento).first()
    except Exception as e:
        logger.error(f"Erro ao buscar pagamento com id {id_pagamento}: {e}")
        raise
