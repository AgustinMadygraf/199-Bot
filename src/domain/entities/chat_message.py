"""
Path: src/domain/entities/chat_message.py
"""

from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str
    content: str