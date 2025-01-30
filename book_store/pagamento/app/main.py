from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import random
import requests
import os
from . import models
from .databases import engine, get_db
from . import logger

# Obetem url dos serviços ordem de compra
ORDER_URL = os.getenv("ORDER_URL", "http://ordem_de_compra:8081")

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Define a rota para processar pagamento
@app.post("/pagamentos", response_model=models.Pagamento)
def processar_pagamento(pagamento: models.PagamentoCreate, db: Session = Depends(get_db)):
    """
    Processa um pagamento para a ordem especificada
    """
    try:
        # Valida se a ordem de compra existe
        ordem_response = requests.get(f"{ORDER_URL}/ordens/{pagamento.id_ordem}")
        if ordem_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Ordem de compra não encontrada")
        
        # Processa pagamento
        status = random.choice(["Aprovado", "Recusado"])
        
        # Cria o pagamento no banco
        db_pagamento = models.processar_pagamento(db=db, pagamento=pagamento, status=status)
        
        return db_pagamento
    except Exception as e:
        logger.error(f"Erro ao processar pagamento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar pagamento: {str(e)}")

@app.get("/pagamentos/{id_pagamento}", response_model=models.Pagamento)
def lista_pagamentos(id_pagamento: int, db: Session = Depends(get_db)):
    """
    Retorna informações de um pagamento pelo ID
    """
    db_pagamento = models.lista_pagamentos(db=db, id_pagamento=id_pagamento)
    if db_pagamento is None:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return db_pagamento
