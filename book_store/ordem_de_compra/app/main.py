"""
Função principal que cria a aplicação FastAPI
"""
import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import requests
from . import models
from .databases import engine, get_db
from . import logger

# Obetem url dos serviços pagamento e cadastro de livros
PAYMENT_URL = os.getenv("PAYMENT_URL", "http://pagamento:8082")
BOOK_URL = os.getenv("BOOK_URL", "http://cadastro_de_livros:8080")

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI()

# Define a rota para criar uma ordem
@app.post("/ordens/", response_model=models.Ordem)
def cria_ordem(ordem: models.OrdemCreate, db: Session = Depends(get_db)):
    """
    Rota para criar uma ordem de compra de um livro
    """
    try:
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
        
        return db_ordem
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar ordem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar ordem {str(e)}")

# Define a rota para listar ordens por id
@app.get("/ordens/{id}", response_model=models.Ordem)
def busca_ordem(id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar uma ordem pelo id
    """
    try:
        logger.info(f"Buscando ordem com id: {id}")
        ordem = models.lista_ordem(db=db, id_ordem=id)
        if ordem is None:
            logger.warning(f"Ordem com id {id} não encontrada")
            raise HTTPException(status_code=404, detail="Ordem não encontrada")
        return ordem
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar ordem: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar ordem")
