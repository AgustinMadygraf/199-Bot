"""
Path: src/infrastructure/f1/prompt_repository.py
"""

import json
from pathlib import Path
from typing import List
from src.application.ports.tutor_ports import PromptRepository

class FilePromptRepository(PromptRepository):
    def __init__(self):
        self.base_path = Path(__file__).resolve().parents[3] / "data"
        self.prompt_path = self.base_path / "prompts" / "tutor_system.md"
        self.config_path = self.base_path / "config" / "frases_prohibidas.json"

    def obtener_system_prompt(self) -> str:
        try:
            return self.prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return "Eres un experto en F1. (Error: archivo de prompt no encontrado)"

    def obtener_frases_prohibidas(self) -> List[str]:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
