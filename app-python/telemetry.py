"""
Módulo para configuração sinais de telemetria
"""
import logging 
from pythonjsonlogger import jsonlogger

def setup_logging():
    """
    Configura logging para enviar logs em formato JSON
    """
    logger = logging.getLogger()
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger
"""
Retorna o logger configurado
"""
logger = setup_logging()
