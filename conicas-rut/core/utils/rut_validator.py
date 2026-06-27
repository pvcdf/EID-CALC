# conicas-rut/core/utils/rut_validator.py

from core.utils.result_models import build_success, build_error


# ── Limpieza y variable auxiliar ──────────────────────────────────────────

def clean_rut(rut: str) -> str:
    """Elimina puntos, guion y espacios del RUT."""
    return (
        rut.replace(".", "")
           .replace("-", "")
           .replace(" ", "")
           .upper()
    )


def compute_v(dv: str) -> int:
    """
    Calcula la variable auxiliar v usada en coeficientes.

    Reglas:
        K → 10
        0 → 11
        1...9 → su valor numérico
    """
    if dv == "K":
        return 10

    if dv == "0":
        return 11

    if dv.isdigit():
        return int(dv)

    return -1


# ── Validación módulo 11 ──────────────────────────────────────────────────
# Proceso:
# 1. Limpiar RUT.
# 2. Multiplicar dígitos de derecha a izquierda por [2, 3, 4, 5, 6, 7].
# 3. Sumar productos.
# 4. Calcular 11 - (suma % 11).
# 5. Comparar el DV esperado con el DV ingresado.

def validate_rut(rut: str) -> dict:
    """Valida un RUT chileno usando módulo 11 y guarda los pasos del cálculo."""
    steps: list[str] = []

    if not rut or not isinstance(rut, str):
        return build_error(error="RUT vacío o tipo inválido.")

    clean = clean_rut(rut)
    steps.append(f"RUT limpio: {clean}")

    if len(clean) < 2:
        return build_error(
            error="RUT demasiado corto.",
            steps=steps,
        )

    body = clean[:-1]    # cuerpo numérico del RUT
    dv_input = clean[-1] # dígito verificador ingresado

    if not (dv_input.isdigit() or dv_input == "K"):
        return build_error(
            error=f"DV '{dv_input}' no es válido. Debe ser 0-9 o K.",
            steps=steps,
        )

    if not body.isdigit():
        return build_error(
            error="El cuerpo del RUT debe tener solo números.",
            steps=steps,
        )

    if len(body) != 8:
        return build_error(
            error=f"El cuerpo debe tener 8 dígitos. Tiene {len(body)}.",
            steps=steps,
        )

    digits = [int(digit) for digit in body]  # dígitos d1...d8

    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    multiplier_index = 0

    steps.append("Proceso módulo 11:")

    # Se recorre desde el último dígito hacia el primero.
    for digit in digits[::-1]:
        multiplier = multipliers[multiplier_index % len(multipliers)]
        product = digit * multiplier

        total += product

        steps.append(f"{digit} × {multiplier} = {product}")

        multiplier_index += 1

    remainder = total % 11
    result = 11 - remainder

    steps.append(f"Suma total = {total}")
    steps.append(f"{total} % 11 = {remainder}")
    steps.append(f"11 - {remainder} = {result}")

    if result == 11:
        dv_expected = "0"
    elif result == 10:
        dv_expected = "K"
    else:
        dv_expected = str(result)

    steps.append(f"DV esperado = {dv_expected}")
    steps.append(f"DV ingresado = {dv_input}")

    is_valid = dv_expected == dv_input

    if not is_valid:
        return build_error(
            error=f"DV incorrecto: ingresó '{dv_input}', se esperaba '{dv_expected}'.",
            steps=steps,
            data={
                "clean_rut": clean,
                "body": body,
                "dv_input": dv_input,
                "dv_expected": dv_expected,
            },
        )

    v = compute_v(dv_input)

    return build_success(
        explanation="El RUT es válido.",
        steps=steps,
        data={
            "clean_rut": clean,        # RUT sin formato
            "body": body,              # cuerpo sin DV
            "digits": digits,          # lista de dígitos numéricos
            "named_digits": {          # dígitos etiquetados para cónicas y límites
                f"d{i + 1}": digits[i]
                for i in range(8)
            },
            "dv_input": dv_input,      # DV ingresado
            "dv_expected": dv_expected,# DV calculado por módulo 11
            "v": v,                    # variable auxiliar para coeficientes
        },
    )