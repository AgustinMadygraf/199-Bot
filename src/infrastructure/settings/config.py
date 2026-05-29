import os
from dotenv import load_dotenv

def cargar_configuracion():
    """Carga las variables de entorno."""
    load_dotenv()
    
    # Verificación básica de variables críticas
    if not os.environ.get("TELEGRAM_TOKEN"):
        raise ValueError("La variable de entorno TELEGRAM_TOKEN no está configurada.")
    
    # Podrías agregar otras verificaciones aquí
    return True
