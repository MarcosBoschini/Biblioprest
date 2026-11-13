# Criterios de aceptación

> Formato Dado / Cuando / Entonces. Fecha de referencia: hoy = 2026-11-13.

## AT-01 (RN-01) ISBN duplicado
- **Dado** un libro con ISBN 9780001
- **Cuando** intento registrar otro libro con ISBN 9780001
- **Entonces** recibo 409 "El ISBN ya está registrado."

## AT-02 (RN-02, RN-07) Préstamo exitoso
- **Dado** un Estudiante sin deudas y un libro con 2 copias disponibles
- **Cuando** registro el préstamo el 2026-11-13
- **Entonces** el vencimiento es 2026-11-20 y las copias disponibles pasan a 1

## AT-03 (RN-02) Sin copias
- **Dado** un libro con 0 copias disponibles
- **Cuando** intento prestarlo
- **Entonces** recibo 409 "No hay copias disponibles."

## AT-04 (RN-03) Límite por tipo
- **Dado** un Externo con 2 préstamos activos
- **Cuando** intento un tercer préstamo
- **Entonces** recibo 409 "El socio alcanzó su límite de préstamos."

## AT-05 (RN-04) Socio con vencidos
- **Dado** un socio con un préstamo vencido
- **Cuando** intento un préstamo nuevo
- **Entonces** recibo 409 "El socio tiene préstamos vencidos."

## AT-06 (RN-05) Socio con multa
- **Dado** un socio con saldo de multa $100
- **Cuando** intento un préstamo nuevo
- **Entonces** recibo 409 "El socio tiene multas impagas."

## AT-07 (RN-06) Mismo libro dos veces
- **Dado** un socio con el libro X en préstamo activo
- **Cuando** intento prestarle otra copia del libro X
- **Entonces** recibo 409 "El socio ya tiene este libro en préstamo."

## AT-08 (RN-08) Renovación válida
- **Dado** un Docente con préstamo vigente que vence el 2026-11-20, sin renovar
- **Cuando** renuevo
- **Entonces** el nuevo vencimiento es 2026-12-04 y `renovado = true`

## AT-09 (RN-09) Renovación rechazada
- **Dado** un préstamo ya renovado, o vencido
- **Cuando** intento renovar
- **Entonces** recibo 409 "El préstamo no puede renovarse."

## AT-10 (RN-10) Devolución a tiempo
- **Dado** un préstamo que vence el 2026-11-20
- **Cuando** lo devuelvo el 2026-11-19
- **Entonces** multa = $0 y las copias disponibles suben en 1

## AT-11 (RN-10) Devolución con atraso
- **Dado** un Estudiante con préstamo vencido el 2026-11-10
- **Cuando** devuelve el 2026-11-13 (3 días de atraso)
- **Entonces** multa = 3 × $100 = $300 y el saldo del socio sube $300

## AT-12 (RN-13) Pago de multa
- **Dado** un socio con saldo $300
- **Cuando** paga $100
- **Entonces** el saldo queda en $200
- **Y cuando** intenta pagar $500, recibe 400 "El pago supera el saldo."

## AT-13 (RN-11) Baja de libro
- **Dado** un libro con una copia prestada
- **Cuando** intento eliminarlo
- **Entonces** recibo 409 y el libro sigue existiendo

## AT-14 (RN-12, RN-14) Socio dado de baja
- **Dado** un socio con préstamos activos
- **Cuando** intento darlo de baja
- **Entonces** recibo 409
