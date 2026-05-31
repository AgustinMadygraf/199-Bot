"""
Path: src/infrastructure/rag_indexer.py
"""

import os
from src.infrastructure.pdf_service import PDFService
from src.infrastructure.db.chroma_vector_repository import ChromaVectorRepository
from src.infrastructure.settings.logger import logger

class RAGIndexer:
    def __init__(self, repository: ChromaVectorRepository, pdf_service: PDFService):
        self.repository = repository
        self.pdf_service = pdf_service
        self.PDF_DIR = "reglamento_pdfs"

    def indexar(self):
        if self.repository.count() > 0:
            logger.info(f"✅ Base vectorial ya cuenta con datos indexados ({self.repository.count()} fragmentos)")
            return

        logger.info("📚 Iniciando indexación del reglamento FIA 2026...")
        
        # Asumimos que los PDFs ya están descargados
        if not os.path.exists(self.PDF_DIR):
            logger.warning(f"⚠️ No existe la carpeta {self.PDF_DIR}")
            return
            
        pdfs = [os.path.join(self.PDF_DIR, f) for f in os.listdir(self.PDF_DIR) if f.endswith(".pdf")]
        
        if not pdfs:
            logger.warning("⚠️ No hay PDFs para indexar")
            return

        todos = []
        for pdf in pdfs:
            fragmentos = self.pdf_service.extraer_texto(pdf)
            todos.extend(fragmentos)
            logger.info(f"   {os.path.basename(pdf)}: {len(fragmentos)} fragmentos")

        # Indexar en lotes
        LOTE = 100
        for i in range(0, len(todos), LOTE):
            lote = todos[i:i + LOTE]
            textos = [f["texto"] for f in lote]
            ids = [f"doc_{i + j}" for j in range(len(lote))]
            metas = [{"tipo": "pdf_reglamento", "fuente": f["fuente"], "pagina": f["pagina"]} for f in lote]
            self.repository.add_texts(textos, metas, ids)

        logger.info(f"✅ Indexación completa: {len(todos)} fragmentos en ChromaDB")
