"""
Módulo para configuração sinais de telemetria
"""
import logging 
from pythonjsonlogger import jsonlogger

def setup_logging():
    """
    Configura logging para enviar logs em formato JSON
    """
    logger = logging.getLogger(__name__) # Cria um logger
    if not logger.handlers: # Evita adicionar mais de um handler, evita logs duplicados   
        logHandler = logging.StreamHandler() # Envia logs para a saída padrão (stdout)
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s ') # Formatação do log
        logHandler.setFormatter(formatter) # Aplica a formatação ao handler
        logger.addHandler(logHandler) # Adiciona o handler ao logger
        logger.setLevel(logging.INFO) # Define o nível de log como INFO
    return logger
"""
Retorna o logger configurado
"""
logger = setup_logging()
