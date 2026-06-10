# conicas-rut/core/value_table.py

def CrearTablaValores(a, funcion):
    """
    Genera la tabla de valores numéricos evaluados cerca de 'a' por ambos lados.

    Izquierda : a-1, a-0.1, a-0.01, a-0.001 
    Derecha   : a+0.001, a+0.01, a+0.1, a+1 
    """
    deltas_izq = [-1, -0.1, -0.01, -0.001]
    deltas_der = [0.001, 0.01, 0.1, 1]

    def _evaluar(delta):
        x = round(a + delta, 6)
        try:
            y = funcion(x)
        except (ZeroDivisionError, ValueError):
            y = None
        return {"x": x, "y": y}

    return {
        "izquierda": [_evaluar(d) for d in deltas_izq],
        "derecha":   [_evaluar(d) for d in deltas_der],
    }


def ultimo_valor(filas: list) -> float | None:
    """
    Retorna el último valor y no nulo de una lista de filas.
    Útil para que limit_analyzer extraiga el límite numérico aproximado.
    """
    return next(
        (f["y"] for f in reversed(filas) if f["y"] is not None),
        None
    )