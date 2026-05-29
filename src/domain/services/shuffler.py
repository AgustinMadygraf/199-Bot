"""
Path: src/domain/services/shuffler.py
"""

from typing import List, TypeVar, Protocol

T = TypeVar('T')

class ListShuffler(Protocol):
    def shuffle(self, items: List[T]) -> List[T]:
        ...
