"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import re

class TelegramTokenFilter(logging.Filter):
    """Filtra el token del bot de los logs para que no aparezca en pantalla."""
    def filter(self, record):
        msg = record.getMessage()
        # Oculta el token en las URLs de las peticiones HTTP
        record.msg = re.sub(r'bot[a-zA-Z0-9_\-]+', 'bot[TOKEN_OCULTO]', msg)
        return True

# Creamos la instancia del logger
logger = logging.getLogger("f1bot")
logger.setLevel(logging.INFO)

def setup_logging():
    """Configuración centralizada del logger global."""
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    
    # Aplicar el filtro al logger principal
    logger.addHandler(handler)
    logger.addFilter(TelegramTokenFilter())
    
    # También configuramos httpx para que use el filtro
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.addHandler(handler)
    httpx_logger.addFilter(TelegramTokenFilter())
    
    logger.info("⚙️ Logger configurado correctamente.")
