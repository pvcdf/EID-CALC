<<<<<<< HEAD
# conicas-rut/core/rut_validator.py

from core.result_models import build_success, build_error

# Limpieza de RUT
def clean_rut(rut: str) -> str:
    """
    Elimina puntos, guiones y espacios.
    Convierte DV a mayúscula.
    """

    rut = (
        rut.replace(".", "")
           .replace("-", "")
           .replace(" ", "")
    )

    return rut.upper()


# Variable auxiliar v
def compute_v(dv: str) -> int:
    """
    Calcula la variable auxiliar v.

    Reglas:
        v = 10  si DV = K
        v = 11  si DV = 0
        v = DV  si DV ∈ {1..9}
    """

    if dv == "K":
        return 10

    if dv == "0":
        return 11

    if dv.isdigit():
        return int(dv)

    return -1

# Validación principal
def validate_rut(rut: str) -> dict:

    steps = []
    # Validaciones básicas
    if not rut or not isinstance(rut, str):
        return build_error( error="RUT vacío o tipo inválido")

    clean = clean_rut(rut)
    steps.append(f"RUT limpio: {clean}")

    if len(clean) < 2:

        return build_error(
            error="RUT demasiado corto",
            steps=steps
        )
=======


def clean_rut(rut: str) -> str:
    """Elimina puntos, guiones y espacios. Convierte DV a mayúscula."""
    rut = rut.replace(".", "").replace("-", "").replace(" ", "")
    return rut.upper()

def clean_rut(rut: str) -> str:
    """Elimina puntos, guiones y espacios. Convierte DV a mayúscula."""
    rut = rut.replace(".", "").replace("-", "").replace(" ", "")
    return rut.upper()


def compute_v(dv: str) -> int:
    """
    Calcula la variable auxiliar v según:
      v = 10  si DV = K
      v = 11  si DV = 0
      v = DV  si DV ∈ {1..9}
    Retorna -1 si el DV no es válido (para manejo de errores).
    """
    if dv == "K":
        return 10
    if dv == "0":
        return 11
    if dv.isdigit():
        return int(dv)
    return -1


def validate_rut(rut: str) -> dict:
    """
    Valida un RUT usando módulo 11.
    Retorna toda la información necesaria para coef_builder y tramo_function.
    El cuerpo debe tener exactamente 8 dígitos (d1..d8).
    """
    steps = []

    if not rut or not isinstance(rut, str):
        return {"valid": False, "error": "RUT vacío o tipo inválido"}

    clean = clean_rut(rut)

    if len(clean) < 2:
        return {"valid": False, "error": "RUT demasiado corto"}
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))

    body = clean[:-1]
    dv_input = clean[-1]

<<<<<<< HEAD
    # Validar DV
    if not (
        dv_input.isdigit()
        or dv_input == "K"
    ):

        return build_error(
            error=(
                f"DV '{dv_input}' no es válido "
                f"(debe ser 0-9 o K)"
            ),
            steps=steps
        )

    # Validar cuerpo
    if not body.isdigit():

        return build_error(
            error=(
                "El cuerpo del RUT "
                "debe contener solo números"
            ),
            steps=steps
        )

    if len(body) != 8:

        return build_error(
            error=(
                f"El cuerpo debe tener "
                f"exactamente 8 dígitos "
                f"(tiene {len(body)})"
            ),
            steps=steps
        )
=======
    # Validar que el DV sea un carácter legal
    if not (dv_input.isdigit() or dv_input == "K"):
        return {"valid": False, "error": f"DV '{dv_input}' no es válido (debe ser 0-9 o K)"}

    # El PDF asume exactamente 8 dígitos en el cuerpo
    if not body.isdigit():
        return {"valid": False, "error": "El cuerpo del RUT debe contener solo números"}

    if len(body) != 8:
        return {
            "valid": False,
            "error": f"El cuerpo debe tener exactamente 8 dígitos (tiene {len(body)})"
        }
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))

    digits = [int(d) for d in body]

    # Algoritmo módulo 11
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    multiplier_index = 0
    reversed_digits = digits[::-1]
<<<<<<< HEAD
    steps.append("Proceso módulo 11:")

    for digit in reversed_digits:
        multiplier = (
            multipliers[
                multiplier_index % len(multipliers)
            ]
        )

        product = digit * multiplier

        total += product

        steps.append(
            f"{digit} × {multiplier} = {product}"
        )

=======

    steps.append("Proceso módulo 11:")
    for digit in reversed_digits:
        multiplier = multipliers[multiplier_index % len(multipliers)]
        product = digit * multiplier
        total += product
        steps.append(f"  {digit} × {multiplier} = {product}")
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
        multiplier_index += 1

    remainder = total % 11
    result = 11 - remainder

    steps.append(f"Suma total = {total}")
    steps.append(f"{total} % 11 = {remainder}")
    steps.append(f"11 - {remainder} = {result}")

<<<<<<< HEAD
    # ─────────────────────────────────────────
    # DV esperado
    # ─────────────────────────────────────────

    if result == 11:
        dv_expected = "0"

    elif result == 10:
        dv_expected = "K"

=======
    if result == 11:
        dv_expected = "0"
    elif result == 10:
        dv_expected = "K"
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
    else:
        dv_expected = str(result)

    steps.append(f"DV esperado = {dv_expected}")
    steps.append(f"DV ingresado = {dv_input}")

    valid = dv_expected == dv_input

<<<<<<< HEAD
    # ─────────────────────────────────────────
    # Variable auxiliar v
    # ─────────────────────────────────────────

    if valid:
        v = compute_v(dv_input)

    else:
        v = compute_v(dv_expected)

    # ─────────────────────────────────────────
    # Error DV incorrecto
    # ─────────────────────────────────────────

    if not valid:

        return build_error(
            error=(
                f"DV incorrecto: ingresó "
                f"'{dv_input}', se esperaba "
                f"'{dv_expected}'"
            ),
            steps=steps,
            data={
                "clean_rut": clean,
                "body": body,
                "dv_input": dv_input,
                "dv_expected": dv_expected,
            }
        )

    # ─────────────────────────────────────────
    # Resultado exitoso
    # ─────────────────────────────────────────

    return build_success(
        explanation="El RUT es válido.",
        steps=steps,
        data={
            "clean_rut": clean,
            "body": body,
            "digits": digits,
            "named_digits": {
                f"d{i+1}": digits[i]
                for i in range(8)
            },
            "dv_input": dv_input,
            "dv_expected": dv_expected,
            "v": v,
        }
    )
=======
    # v es necesario para coef_builder (denominador de A y B)
    v = compute_v(dv_input) if valid else compute_v(dv_expected)

    return {
        "valid": valid,
        "error": f"DV incorrecto: ingresó '{dv_input}', se esperaba '{dv_expected}'" if not valid else None,
        "clean_rut": clean,
        "body": body,
        "digits": digits,
        "named_digits": {
            f"d{i+1}": digits[i] for i in range(8)
        },
        "dv_input": dv_input,
        "dv_expected": dv_expected,
        "v": v,
        "steps": steps
    }
>>>>>>> parent of 2154406 (ACTUALIZACIÓN DE ARCHIVOS (ELIMINADOS Y MODIFICADOS))
