# Roadmap 199-Bot Refactor

## Prioridad Alta: Desacoplamiento de Datos
- [x] **Crear Puerto de Prompts:** Definir PromptRepository en src/application/ports/tutor_ports.py para abstraer la obtención de plantillas de IA.
- [x] **Extraer System Prompt:** Mover el texto del prompt de TutorUseCase.py a un archivo Markdown en data/prompts/tutor_system.md.
- [x] **Implementar Adaptador de Archivos:** Crear FilePromptRepository en infraestructura para leer los archivos .md.
- [x] **Externalizar Filtros:** Mover la lista de frases_prohibidas a un archivo JSON o YAML en data/config/.

## Prioridad Media: Refactorización de Lógica
- [x] **Limpieza de TutorUseCase:** Inyectar el nuevo puerto en el constructor y eliminar todos los strings hardcodeados.
- [x] **Generación Dinámica:** Cambiar la construcción del prompt para que se realice en cada consulta.
- [ ] **Domain Service de Limpieza:** Considerar mover la lógica de _limpiar_texto a un servicio de dominio.

## Prioridad Baja: Calidad y Extensión
- [x] **Tests Unitarios:** Crear pruebas que validen que el bot responde correctamente usando prompts cargados desde archivos temporales (Mocks).
- [ ] **Soporte Multilingüe:** Preparar la estructura de carpetas de prompts para admitir /en/, /es/, etc.
- [ ] **Refactorizar QuizController:** Analizar y aplicar DDD/SOLID para desacoplar lógica de presentación y mejorar extensibilidad.
- [ ] **Desacoplar Preguntas de Entidades:** Extraer PREGUNTAS_POOL de src/domain/entities/quiz.py a un archivo externo (JSON/YAML) e implementar un QuizRepository para cargarlas dinámicamente.
- [ ] **Persistencia de Estado:** Evaluar mover el estado de QuizSession de memoria a una base de datos (ej: Redis o SQLite) para evitar pérdida de progreso al reiniciar.

---
*Este TODO fue generado tras el análisis técnico del 31 de mayo de 2026.*
