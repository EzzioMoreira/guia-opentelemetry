"""
Módulo responsável por criar a conexão com o banco de dados
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from . import logger

# Obtém as credenciais do banco de dados das variáveis de ambiente
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")

# URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# Cria a engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Verifica e cria o banco de dados, caso necessário
def initialize_database():
    """
    Inicializa o banco de dados, criando-o se não existir.
    """
    try:
        if not database_exists(engine.url):
            logger.info(f"Banco de dados {DB_NAME} não existe. Criando...")
            create_database(engine.url)
        else:
            logger.info(f"Banco de dados {DB_NAME} já existe.")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {e}")
        raise

initialize_database()

# Configura a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função que retorna uma sessão do banco de dados
def get_db():
    """
    Obtém uma nova sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Conexão com o banco de dados encerrada.")
