# Modelo de datos

## Libro (`libros`)
| Campo | Tipo | Restricción |
|---|---|---|
| id | entero | PK, autoincremental |
| isbn | texto | Único, obligatorio |
| titulo | texto | Obligatorio |
| autor | texto | Obligatorio |
| copias_totales | entero | ≥ 1 |
| copias_disponibles | entero | 0 ≤ valor ≤ copias_totales |

## Socio (`socios`)
| Campo | Tipo | Restricción |
|---|---|---|
| id | entero | PK |
| nombre | texto | Obligatorio |
| documento | texto | Único, obligatorio |
| tipo | texto | `ESTUDIANTE` \| `DOCENTE` \| `EXTERNO` |
| saldo_multas | entero | ≥ 0, por defecto 0 |
| activo | booleano | Por defecto verdadero |

## Préstamo (`prestamos`)
| Campo | Tipo | Restricción |
|---|---|---|
| id | entero | PK |
| libro_id | entero | FK → libros |
| socio_id | entero | FK → socios |
| fecha_prestamo | fecha | Obligatorio |
| fecha_vencimiento | fecha | Obligatorio |
| fecha_devolucion | fecha | Nulo mientras esté activo |
| renovado | booleano | Por defecto falso |
| multa | entero | ≥ 0, se calcula al devolver |

## Relaciones
```
Socio 1 ──── N Préstamo N ──── 1 Libro
```

## Configuración de políticas (constante en código)
```
ESTUDIANTE: max=3, dias=7,  tarifa=100
DOCENTE:    max=5, dias=14, tarifa=50
EXTERNO:    max=2, dias=5,  tarifa=200
```
