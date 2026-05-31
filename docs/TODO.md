# TODO: Roadmap de Refactorización

## Fase 1: Preparación (Completado)
- [x] Definir Entidades de Dominio.
- [x] Definir contratos (Protocolos) para Gateways/Repositorios.
- [x] Centralizar lógica de tiempo.

## Fase 2: Implementación de Infraestructura (En progreso)
- [x] Crear F1ApiGateway en src/infrastructure/f1_api_gateway.py.
- [x] Migrar lógica de get_last_race_results a F1ApiGateway.
- [ ] Refactorizar F1KnowledgeRepository:
    - [x] Implementar src/application/ports/tutor_ports.py/KnowledgeRepository.
    - [ ] Crear adaptador para f1_rag.py (en progreso).
    - [ ] Separar lógica de orquestación (RAG vs API) fuera de la clase.
- [ ] Refactorizar src/infrastructure/f1_api.py:
    - [ ] Migrar funciones restantes a F1ApiGateway o eliminarlas.
- [ ] **Refactorizar SystemController (Nuevo):**
    - [ ] Definir protocolo `HistoryGateway`.
    - [ ] Implementar método `borrar` en `DBHistoryRepository`.
    - [ ] Crear `AudioUseCase` para encapsular lógica de archivos y transcripción.
    - [ ] Eliminar dependencias de `os` y módulos `db` en `SystemController`.

## Fase 3: Testing y Validación (Pendiente)
- [ ] Crear Mocks para F1Gateway y KnowledgeRepository para tests unitarios.
- [ ] Actualizar/Crear tests para F1ApiGateway sin realizar llamadas HTTP reales.

## Fase 4: Integración (Pendiente)
- [ ] Actualizar main.py para inyectar correctamente F1KnowledgeRepository implementado.
