# Plan de Acción: Refactorización TutorUseCase

## Prioridad Alta: Desacoplamiento de Datos
- [x] **Crear Puerto de Prompts:** Definir `PromptRepository` en `src/application/ports/tutor_ports.py` para abstraer la obtención de plantillas de IA.
- [x] **Extraer System Prompt:** Mover el texto del prompt de `TutorUseCase.py` a un archivo Markdown en `data/prompts/tutor_system.md`.
- [x] **Implementar Adaptador de Archivos:** Crear `FilePromptRepository` en infraestructura para leer los archivos `.md`.
- [x] **Externalizar Filtros:** Mover la lista de `frases_prohibidas` a un archivo `JSON` o `YAML` en `data/config/`.

## Prioridad Media: Refactorización de Lógica
- [x] **Limpieza de TutorUseCase:** Inyectar el nuevo puerto en el constructor y eliminar todos los strings hardcodeados.
- [x] **Generación Dinámica:** Cambiar la construcción del prompt para que se realice en cada consulta (o mediante un método `get_prompt()`), asegurando que tome los datos más recientes del repositorio de conocimiento.
- [ ] **Domain Service de Limpieza:** Considerar mover la lógica de `_limpiar_texto` a un servicio de dominio si las reglas se vuelven más complejas.

## Prioridad Baja: Calidad y Extensión
- [x] **Tests Unitarios:** Crear pruebas que validen que el bot responde correctamente usando prompts cargados desde archivos temporales (Mocks).
- [ ] **Soporte Multilingüe:** Preparar la estructura de carpetas de prompts para admitir `/en/`, `/es/`, etc.

---
*Este TODO fue generado tras el análisis técnico del 31 de mayo de 2026.*
