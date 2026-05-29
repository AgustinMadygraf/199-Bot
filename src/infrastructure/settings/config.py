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

def obtener_groq_api_key():
    """Retorna la API Key de Groq."""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("Falta la variable de entorno GROQ_API_KEY")
    return key

def obtener_tiempo_minimo_consulta():
    """Retorna el tiempo mínimo entre consultas (Rate Limiting)."""
    return float(os.environ.get("RATE_LIMIT_SECONDS", 2.0))
