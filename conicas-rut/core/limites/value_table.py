# conicas-rut/core/limites/value_table.py


# ── Tabla de aproximación al punto crítico ─────────────────────────────────
# Genera valores cercanos a x = a para observar el comportamiento lateral.

def CrearTablaValores(a, funcion):
    """Genera una tabla de valores cercanos al punto crítico a."""
    deltas_izq = [-1, -0.1, -0.01, -0.001]
    deltas_der = [0.001, 0.01, 0.1, 1]

    def _evaluar(delta):
        x = round(a + delta, 6)  # valor cercano al punto crítico

        try:
            y = funcion(x)

            if isinstance(y, float):
                y = round(y, 6)

        except (ZeroDivisionError, ValueError):
            y = None             # punto no definido o asíntota

        return {
            "x": x,               # valor evaluado
            "y": y,               # resultado de f(x)
        }

    return {
        "izquierda": [_evaluar(delta) for delta in deltas_izq],  # valores x < a
        "derecha": [_evaluar(delta) for delta in deltas_der],    # valores x > a
    }


def ultimo_valor(filas: list) -> float | None:
    """Retorna el último valor definido de una lista de filas."""
    return next(
        (fila["y"] for fila in reversed(filas) if fila["y"] is not None),
        None,
    )