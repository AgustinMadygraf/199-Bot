# Guía de Instalación - 199 Bot

Este documento detalla los pasos necesarios para configurar el entorno de desarrollo y poner en marcha el **199 Bot**.

## Requisitos Previos

- **Python 3.10** o superior.
- **pip** (gestor de paquetes de Python).
- Un token de bot de Telegram (obtenido a través de [@BotFather](https://t.me/BotFather)).
- Una API Key de **Groq** (opcional, para transcripción de audio y tutoría).
- Una API Key de **OpenWeather** (opcional, para consultas de clima).

## Pasos para la Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/199-Bot.git
cd 199-Bot
```

### 2. Crear un Entorno Virtual

Se recomienda el uso de un entorno virtual para aislar las dependencias del proyecto.

```bash
python3 -m venv venv
```

### 3. Activar el Entorno Virtual

- **En Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```
- **En Windows (PowerShell):**
  ```bash
  .\venv\Scripts\Activate.ps1
  ```

### 4. Instalar Dependencias

Con el entorno virtual activado, ejecuta:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configuración de Variables de Entorno

El bot requiere ciertas claves para funcionar. Copia el archivo de ejemplo y edítalo con tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` y completa los siguientes campos:

- `TELEGRAM_TOKEN`: Tu token de Telegram.
- `GROQ_API_KEY`: Tu clave de API de Groq.
- `OPENWEATHER_API_KEY`: Tu clave de API de OpenWeather.

### 6. Ejecución del Bot

Una vez configurado todo, puedes iniciar el bot ejecutando:

```bash
python main.py
```

## Pruebas

Para verificar que todo funciona correctamente, puedes ejecutar los tests unitarios:

```bash
pytest
```
