from typing import Dict, Any

class ControllerRegistry:
    def __init__(self):
        self._controllers: Dict[str, Any] = {}

    def register(self, name: str, controller: Any):
        self._controllers[name] = controller

    def get(self, name: str) -> Any:
        if name not in self._controllers:
            raise ValueError(f"Controlador no registrado: {name}")
        return self._controllers[name]
