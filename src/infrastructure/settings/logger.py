import logging
import re

class TelegramTokenFilter(logging.Filter):
    """Filtra el token del bot de los logs para que no aparezca en pantalla."""
    def filter(self, record):
        msg = record.getMessage()
        # Oculta el token en las URLs de las peticiones HTTP
        record.msg = re.sub(r'bot[a-zA-Z0-9_\-]+', 'bot[TOKEN_OCULTO]', msg)
        return True

def setup_logging():
    """Configuración centralizada del logger global."""
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.addFilter(TelegramTokenFilter())
    
    logging.info("⚙️ Logger configurado correctamente.")

def info(msg: str):
    """Wrapper para logging.info."""
    logging.info(msg)
