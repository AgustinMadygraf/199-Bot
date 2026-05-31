import os
from pypdf import PdfReader
from src.infrastructure.settings.logger import logger

class PDFService:
    @staticmethod
    def extraer_texto(ruta_pdf: str) -> list[dict]:
        """Extrae texto de un PDF y lo divide en fragmentos."""
        fragmentos = []
        try:
            reader = PdfReader(ruta_pdf)
            nombre = os.path.basename(ruta_pdf)
            for i, pagina in enumerate(reader.pages):
                texto = pagina.extract_text()
                if not texto or len(texto.strip()) < 50:
                    continue
                # Dividir páginas largas en fragmentos de ~600 caracteres
                while len(texto) > 600:
                    corte = texto[:600].rfind(". ")
                    if corte == -1:
                        corte = 600
                    fragmentos.append({
                        "texto": texto[:corte + 1].strip(),
                        "fuente": nombre,
                        "pagina": i + 1,
                    })
                    texto = texto[corte + 1:]
                if texto.strip():
                    fragmentos.append({
                        "texto": texto.strip(),
                        "fuente": nombre,
                        "pagina": i + 1,
                    })
        except Exception as e:
            logger.error(f"Error extrayendo texto de {ruta_pdf}: {e}")
        return fragmentos
