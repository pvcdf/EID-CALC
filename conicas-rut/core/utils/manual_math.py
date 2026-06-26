# conicas-rut/core/utils/manual_math.py

# Este modulo es importante porque aqui hacemos los calculos a mano sin usar math o numpy

PI = 3.141592653589793
TAU = 2 * PI

def abs_value(value):
    # Valor absoluto basico
    return value if value >= 0 else -value

def is_close(a, b, tolerance=0.000001):
    return abs_value(a - b) <= tolerance

def round_value(value: float, digits: int = 4) -> float:
    return round(value, digits)

def sqrt_value(value: float) -> float:
    # Raiz cuadrada real elevando a 0.5 
    if value < 0:
        raise ValueError("No existe raiz real de un numero negativo.")
    return value ** 0.5

def sqrt_newton(value: float, iterations: int = 40) -> float:
    # Sacamos la raiz con newton-raphson
    if value < 0:
        raise ValueError("No existe raiz real de un numero negativo.")
    if value == 0:
        return 0.0

    x = value if value >= 1 else 1.0
    for _ in range(iterations):
        x = (x + value / x) / 2
    return x

def shift_text(variable: str, value: float) -> str:
    # Formatea el texto para que se vea bonito 
    value = round_value(value)
    if value == 0:
        return variable
    if value > 0:
        return f"{variable} − {value}"
    return f"{variable} + {round_value(-value)}"

def normalize_radians(x: float) -> float:
    x = x % TAU
    if x > PI:
        x -= TAU
    return x

def sin_taylor(x: float) -> float:
    # Serie de taylor para sacar el seno a mano y asi poder graficar curvas
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
    # El coseno lo sacamos moviendo el seno
    return sin_taylor(x + PI / 2)

def safe_div(numerator, denominator, default=0):
    if denominator == 0:
        return default
    return numerator / denominator