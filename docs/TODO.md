# Roadmap 199-Bot Refactor

## Fase 1: Arquitectura Limpia y Desacoplamiento (Completado)
- [x] Definir Entidades de Dominio y Puertos.
- [x] Implementar Gateways (API, RAG, LiveKnowledge).
- [x] Refactorizar SystemController (eliminando dependencia directa de infraestructura).
- [x] Implementar AudioUseCase como boundary.
- [x] Refactorizar capa de persistencia (mover a sqlite_handler.py y vaciar __init__.py).

## Fase 2: Mejora de la Capa de Infraestructura (En progreso)
- [ ] Refactorizar sqlite_handler.py de procedimental a orientado a objetos (Implementar HistoryRepository formalmente).
- [x] Segregar responsabilidades: Mover registrar_consulta (métricas) a un MetricsRepository separado.
- [ ] Definir e implementar estrategia de testing para Infraestructura (base de datos en memoria).

## Fase 3: Refactorización Final y Testing (Pendiente)
- [ ] Extract get_circuit_weather into a WeatherGateway.
- [ ] Implementar pruebas unitarias completas con Mocks para todos los Gateways y Use Cases.
- [ ] Eliminar legado (src/infrastructure/f1_api.py).
