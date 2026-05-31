from src.application.ports.rag_gateway import RagGateway
from src.infrastructure.chroma_db_repository import ChromaDBRepository
from src.infrastructure.settings.logger import logger

class F1RagGateway(RagGateway):
    def __init__(self, repository: ChromaDBRepository):
        self.repository = repository

    def buscar_reglamento(self, consulta: str) -> str:
        if self.repository.count() == 0:
            return ""

        try:
            results = self.repository.query(consulta)
            fragmentos = results["documents"][0]
            metadatas = results["metadatas"][0]

            if not fragmentos:
                return ""

            lineas = ["[CONTEXTO DE CONOCIMIENTO EXTRA (REGLAMENTO Y ACTUALIDAD F1)]"]
            for texto, meta in zip(fragmentos, metadatas):
                tipo = meta.get("tipo", "pdf_reglamento")
                
                if tipo == "actualidad_f1":
                    lineas.append(
                        f"— NOTICIA DE ACTUALIDAD RECIENTE (Fuente: {meta.get('fuente', 'RSS F1')}):\n{texto}"
                    )
                else:
                    lineas.append(
                        f"— REGLAMENTO FIA (Archivo: {meta.get('fuente', 'Desconocido')} - pág. {meta.get('pagina', '?')}):\n{texto}"
                    )
                    
            return "\n\n".join(lineas)

        except Exception as e:
            logger.error(f"Error buscando en base vectorial: {e}")
            return ""
