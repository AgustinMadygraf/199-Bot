"""
Path: src/infrastructure/chroma_db_status_adapter.py
"""

from src.infrastructure.chroma_db_repository import ChromaDBRepository

class ChromaDBStatusAdapter:
    def __init__(self, repository: ChromaDBRepository):
        self.repository = repository

    def count_documents(self) -> int:
        return self.repository.count()
