"""
Path: src/application/ports/knowledge_status_port.py
"""

from typing import Protocol

class KnowledgeStatusPort(Protocol):
    def count_documents(self) -> int:
        ...
