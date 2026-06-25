# conicas-rut/core/utils/manual_math.py

"""
Funciones matemáticas y de formato manuales para evitar dependencias externas.
Este módulo centraliza operaciones repetidas en transforms, gráficos y vistas.
"""

PI = 3.141592653589793
TAU = 2 * PI


def abs_value(value):
    """
    Retorna el valor absoluto sin usar abs().
    """
    return value if value >= 0 else -value


def is_close(a, b, tolerance=0.000001):
    """
    Compara dos números reales usando tolerancia.
    """
    return abs_value(a - b) <= tolerance


def round_value(value: float, digits: int = 4) -> float:
    """
    Redondea valores para mostrar en pasos, formas canónicas y data.
    """
    return round(value, digits)


def sqrt_value(value: float) -> float:
    """
    Calcula raíz cuadrada real sin usar math.sqrt.

    Usa potencia 0.5 porque no importa librerías externas.
    """
    if value < 0:
        raise ValueError("No existe raíz real de un número negativo.")

    return value ** 0.5


def sqrt_newton(value: float, iterations: int = 40) -> float:
    """
    Calcula raíz cuadrada usando Newton-Raphson.

    Útil para defender que la raíz también fue implementada manualmente.
    """
    if value < 0:
        raise ValueError("No existe raíz real de un número negativo.")

    if value == 0:
        return 0.0

    x = value if value >= 1 else 1.0

    for _ in range(iterations):
        x = (x + value / x) / 2

    return x


def shift_text(variable: str, value: float) -> str:
    """
    Formatea expresiones del tipo x − h o y − k.

    Ejemplos:
        shift_text("x", 3)  -> "x − 3"
        shift_text("x", -2) -> "x + 2"
        shift_text("x", 0)  -> "x"
    """
    value = round_value(value)

    if value == 0:
        return variable

    if value > 0:
        return f"{variable} − {value}"

    return f"{variable} + {round_value(-value)}"


def normalize_radians(x: float) -> float:
    """
    Normaliza un ángulo en radianes al intervalo [-π, π].
    """
    x = x % TAU

    if x > PI:
        x -= TAU

    return x


def sin_taylor(x: float) -> float:
    """
    Aproxima seno usando serie de Taylor alrededor de 0.

    sin(x) ≈ x − x³/3! + x⁵/5! − x⁷/7! + ...
    """
    x = normalize_radians(x)

    return (
        x
        - (x ** 3) / 6
        + (x ** 5) / 120
        - (x ** 7) / 5040
        + (x ** 9) / 362880
        - (x ** 11) / 39916800
    )


def cos_taylor(x: float) -> float:
    """
    Aproxima coseno usando cos(x) = sin(x + π/2).
    """
    return sin_taylor(x + PI / 2)


def safe_div(numerator, denominator, default=0):
    """
    Divide dos números evitando ZeroDivisionError.
    """
    if denominator == 0:
        return default

    return numerator / denominator