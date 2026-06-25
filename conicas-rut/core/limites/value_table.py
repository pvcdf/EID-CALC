# conicas-rut/core/limites/value_table.py


def CrearTablaValores(a, funcion):
    """
    Genera una tabla de valores cercanos al punto crítico a.

    Izquierda:
        a - 1, a - 0.1, a - 0.01, a - 0.001

    Derecha:
        a + 0.001, a + 0.01, a + 0.1, a + 1
    """
    deltas_izq = [-1, -0.1, -0.01, -0.001]
    deltas_der = [0.001, 0.01, 0.1, 1]

    def _evaluar(delta):
        x = round(a + delta, 6)

        try:
            y = funcion(x)

            if isinstance(y, float):
                y = round(y, 6)

        except (ZeroDivisionError, ValueError):
            y = None

        return {
            "x": x,
            "y": y,
        }

    return {
        "izquierda": [_evaluar(delta) for delta in deltas_izq],
        "derecha": [_evaluar(delta) for delta in deltas_der],
    }


def ultimo_valor(filas: list) -> float | None:
    """
    Retorna el último valor no nulo de una lista de filas.

    Puede usarse para extraer una aproximación numérica desde la tabla.
    """
    return next(
        (fila["y"] for fila in reversed(filas) if fila["y"] is not None),
        None,
    )