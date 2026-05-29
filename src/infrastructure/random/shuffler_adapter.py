"""
Path: src/infrastructure/random/shuffler_adapter.py
"""

import random
from typing import List, TypeVar

T = TypeVar('T')

class RandomShuffler:
    def shuffle(self, items: List[T]) -> List[T]:
        random.shuffle(items)
        return items
