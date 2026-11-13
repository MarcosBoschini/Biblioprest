# Prompts para implementar con IA

## Prompt 1 – Contexto
> Lee `constitution.md`, `spec.md` y `data-model.md`. Implementa solo la tarea T-02 de `tasks.md` con el stack de `plan.md`. No agregues funciones que no estén en la especificación.

## Prompt 2 – Reglas de préstamo
> Implementa T-08 en `services.py`. Valida en este orden: socio activo, vencidos, multas, límite, duplicado, copias. Usa los mensajes exactos de la sección 7 de `spec.md`.

## Prompt 3 – Pruebas
> Genera pruebas pytest para AT-01 a AT-14 de `acceptance-tests.md`. Una prueba por escenario, con la fecha "hoy" inyectada.

## Prompt 4 – Revisión
> Compara el código contra `spec.md`. Lista cada regla RN-xx y dime si está implementada, parcialmente o falta.

## Regla de uso
Si la IA genera algo que contradice la spec, se corrige el código; la spec solo cambia con una decisión explícita registrada.
