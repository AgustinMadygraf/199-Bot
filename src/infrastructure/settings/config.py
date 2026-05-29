import os
from dotenv import load_dotenv

def cargar_configuracion():
    """Carga las variables de entorno."""
    load_dotenv()
    
    # Verificación básica de variables críticas
    if not os.environ.get("TELEGRAM_TOKEN"):
        raise ValueError("La variable de entorno TELEGRAM_TOKEN no está configurada.")
    
    return True

def obtener_token_telegram():
    """Retorna el token de Telegram."""
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Falta la variable de entorno TELEGRAM_TOKEN")
    return token
