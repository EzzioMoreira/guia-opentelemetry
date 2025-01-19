"""
Indica que o diretório é um pacote Python
"""
import logging

# Configuração global de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
