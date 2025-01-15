"""
Modulo responsável por criar a conexão com o banco de dados
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from . import logger

# Obtem as credenciais do banco de dados das variáveis de ambiente
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "bookstore")

# URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Função que aguarda até que o banco de dados esteja disponível
def wait_for_db():
    DB_MAX_CONNECTION_RETRIES = os.getenv("DB_MAX_CONNECTION_RETRIES", 5)
   
    for _ in range(DB_MAX_CONNECTION_RETRIES):
        try:
            # Tentativa de conexão com o banco de dados
            logger.info("Tentando conexão com o banco de dados...")
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.close()
            logger.info("Conexão com o banco de dados estabelecida!")
            break
        except psycopg2.OperationalError as e:
            logger.info(f"Conexão com o banco de dados falhou: {e}")
            time.sleep(1)

wait_for_db()

# Cria a engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função que retorna uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Conexão com o banco de dados  encerrada")
