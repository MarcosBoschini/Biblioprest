# Constitución del proyecto – BiblioPrest

## Propósito
Aplicación sencilla pero funcional para gestionar préstamos de una biblioteca pequeña, aplicando reglas de negocio verificables.

## Principios
1. **La especificación manda.** Ningún código se escribe sin una regla o historia en `spec.md`.
2. **Las reglas de negocio viven en un solo lugar** (capa de servicios), nunca en la interfaz.
3. **Simplicidad primero.** Una sola base de datos local (SQLite), sin autenticación en esta versión.
4. **Todo es verificable.** Cada regla `RN-xx` tiene al menos un escenario en `acceptance-tests.md`.
5. **Errores claros.** Toda regla violada devuelve un mensaje en español y un código HTTP adecuado (400/404/409).
6. **Fechas en UTC, formato ISO 8601.** La multa se calcula por días completos.
7. **La IA propone, la spec decide.** Si el código generado contradice la spec, se corrige el código.

## Fuera de alcance (v1)
Login y roles, reservas de libros, notificaciones por correo, pagos reales de multas, múltiples sedes.
