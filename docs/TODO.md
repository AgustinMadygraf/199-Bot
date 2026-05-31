# Roadmap 199-Bot Refactor

## Prioridad Alta: Desacoplamiento de Datos (Completado)
- [x] **Crear Puerto de Prompts:** Definir PromptRepository en src/application/ports/tutor_ports.py.
- [x] **Extraer System Prompt:** Mover texto a data/prompts/tutor_system.md.
- [x] **Implementar Adaptador de Archivos:** Crear FilePromptRepository.
- [x] **Externalizar Filtros:** Mover frases_prohibidas a data/config/.
- [x] **Desacoplar Preguntas de Entidades:** Extraer PREGUNTAS_POOL a JSON y implementar QuizRepository.

## Prioridad Media: Refactorización de Arquitectura y Limpieza
- [x] **Limpieza de TutorUseCase:** Inyectar puertos y eliminar hardcode.
- [x] **Generación Dinámica:** Cambiar construcción de prompts.
- [ ] **QuizPresenter:** Crear presenter para centralizar el formato visual y emojis del quiz.
- [ ] **QuizController Refactor:** Delegar formateo a QuizPresenter.
- [ ] **Rate Limiting Middleware:** Mover lógica de es_spammer de TelegramBot a un middleware/decorador.
- [ ] **Registry Pattern en Bot:** Desacoplar inyección de controladores en TelegramBot.

## Prioridad Baja: Calidad y Extensión
- [x] **Tests Unitarios:** Pruebas con Mocks para prompts.
- [ ] **Soporte Multilingüe:** Preparar estructura de prompts.
- [ ] **Persistencia de Estado:** Evaluar mover QuizSession a BD (SQLite/Redis).

---
*Este TODO fue actualizado el 31 de mayo de 2026 tras auditoría de arquitectura.*
