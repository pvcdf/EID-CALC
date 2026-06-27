# conicas-rut/core/utils/manual_math.py

# Utilidades matemáticas implementadas sin usar librerias matematicas.

PI = 3.141592653589793
TAU = 2 * PI


# ── Operaciones básicas ───────────────────────────────────────────────────

def abs_value(value):
    """Calcula valor absoluto."""
    return value if value >= 0 else -value


def is_close(a, b, tolerance=0.000001):
    """Compara dos números con tolerancia para evitar errores decimales."""
    return abs_value(a - b) <= tolerance


def round_value(value: float, digits: int = 4) -> float:
    """Redondea un valor numérico a una cantidad fija de decimales."""
    return round(value, digits)


def sqrt_value(value: float) -> float:
    """Calcula raíz cuadrada real usando potencia 0.5."""
    if value < 0:
        raise ValueError("No existe raíz real de un número negativo.")

    return value ** 0.5


def sqrt_newton(value: float, iterations: int = 40) -> float:
    """Calcula raíz cuadrada mediante Newton-Raphson."""
    if value < 0:
        raise ValueError("No existe raíz real de un número negativo.")

    if value == 0:
        return 0.0

    x = value if value >= 1 else 1.0

    for _ in range(iterations):
        x = (x + value / x) / 2

    return x


def safe_div(numerator, denominator, default=0):
    """Divide evitando error por denominador cero."""
    if denominator == 0:
        return default

    return numerator / denominator


# ── Formato algebraico ────────────────────────────────────────────────────

def shift_text(variable: str, value: float) -> str:
    """
    Formatea desplazamientos de forma canónica.

    Ejemplo:
        h = 3  → x - 3
        h = -2 → x + 2
    """
    value = round_value(value)

    if value == 0:
        return variable

    if value > 0:
        return f"{variable} − {value}"

    return f"{variable} + {round_value(-value)}"


# ── Trigonometría manual ──────────────────────────────────────────────────

def normalize_radians(x: float) -> float:
    """Normaliza un ángulo al intervalo [-π, π]."""
    x = x % TAU

    if x > PI:
        x -= TAU

    return x


def sin_taylor(x: float) -> float:
    """Aproxima seno usando serie de Taylor."""
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
    """Aproxima coseno usando cos(x) = sin(x + π/2)."""
    return sin_taylor(x + PI / 2)
