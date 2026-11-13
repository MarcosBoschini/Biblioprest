# Especificación funcional – BiblioPrest v1.0

## 1. Descripción
Sistema web para que un bibliotecario administre libros, socios y préstamos.

## 2. Actor
**Bibliotecario**: único usuario del sistema.

## 3. Glosario
- **Libro/Título**: obra identificada por ISBN.
- **Ejemplar**: copia física; un libro tiene `copias_totales` y `copias_disponibles`.
- **Socio**: persona registrada que puede pedir libros.
- **Préstamo activo**: préstamo sin fecha de devolución.
- **Vencido**: préstamo activo cuya fecha de vencimiento es anterior a hoy.

## 4. Historias de usuario
| ID | Historia |
|---|---|
| HU-01 | Como bibliotecario quiero registrar libros con ISBN, título, autor y cantidad de copias. |
| HU-02 | Como bibliotecario quiero registrar socios con su tipo (Estudiante, Docente, Externo). |
| HU-03 | Como bibliotecario quiero prestar un libro a un socio y ver la fecha de vencimiento. |
| HU-04 | Como bibliotecario quiero renovar un préstamo vigente. |
| HU-05 | Como bibliotecario quiero registrar la devolución y ver la multa si hubo atraso. |
| HU-06 | Como bibliotecario quiero ver los préstamos activos y vencidos. |
| HU-07 | Como bibliotecario quiero registrar el pago de multas de un socio. |
| HU-08 | Como bibliotecario quiero buscar libros por título, autor o ISBN. |

## 5. Reglas de negocio

### 5.1 Política por tipo de socio
| Tipo | Máx. préstamos simultáneos | Días de préstamo | Multa por día de atraso |
|---|---|---|---|
| Estudiante | 3 | 7 | $100 |
| Docente | 5 | 14 | $50 |
| Externo | 2 | 5 | $200 |

### 5.2 Reglas
- **RN-01** El ISBN es único. No se puede registrar dos veces.
- **RN-02** Solo se presta si `copias_disponibles > 0`. Al prestar baja en 1; al devolver sube en 1.
- **RN-03** Un socio no puede superar su máximo de préstamos simultáneos (tabla 5.1).
- **RN-04** Un socio no puede retirar libros si tiene algún préstamo vencido.
- **RN-05** Un socio no puede retirar libros si tiene multas impagas (saldo > 0).
- **RN-06** Un socio no puede tener dos préstamos activos del mismo libro.
- **RN-07** Fecha de vencimiento = fecha de préstamo + días de préstamo del tipo de socio.
- **RN-08** Se permite **una sola renovación** por préstamo. La renovación suma los mismos días del tipo de socio **a partir de la fecha de vencimiento actual**.
- **RN-09** No se puede renovar un préstamo vencido ni uno ya renovado.
- **RN-10** Multa = días de atraso completos × tarifa del tipo de socio. Sin atraso, multa = 0. La multa se suma al saldo del socio.
- **RN-11** No se puede eliminar un libro con préstamos activos. No se puede reducir `copias_totales` por debajo de las copias prestadas.
- **RN-12** No se puede dar de baja a un socio con préstamos activos o multas impagas.
- **RN-13** El pago de multas no puede superar el saldo adeudado y debe ser mayor a 0.
- **RN-14** Un socio de baja (`activo = false`) no puede retirar libros.

## 6. Requisitos no funcionales
- RNF-01: Respuesta de la API en menos de 500 ms en operaciones normales.
- RNF-02: Interfaz web simple, usable en celular.
- RNF-03: Los datos persisten entre reinicios (SQLite).

## 7. Casos de error esperados
| Situación | Código | Mensaje |
|---|---|---|
| ISBN duplicado | 409 | "El ISBN ya está registrado." |
| Sin copias | 409 | "No hay copias disponibles." |
| Límite alcanzado | 409 | "El socio alcanzó su límite de préstamos." |
| Socio con vencidos | 409 | "El socio tiene préstamos vencidos." |
| Socio con multas | 409 | "El socio tiene multas impagas." |
| Libro ya prestado al socio | 409 | "El socio ya tiene este libro en préstamo." |
| Renovación no permitida | 409 | "El préstamo no puede renovarse." |
| Recurso inexistente | 404 | "No encontrado." |
