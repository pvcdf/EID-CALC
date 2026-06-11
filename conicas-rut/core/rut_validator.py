# conicas-rut/core/rut_validator.py

from core.result_models import build_success, build_error


def clean_rut(rut: str) -> str:
    """Elimina puntos, guiones y espacios. Convierte DV a mayúscula."""
    return rut.replace(".", "").replace("-", "").replace(" ", "").upper()


def compute_v(dv: str) -> int:
    """
    Calcula la variable auxiliar v.
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


def validate_rut(rut: str) -> dict:
    steps = []

    if not rut or not isinstance(rut, str):
        return build_error(error="RUT vacío o tipo inválido")

    clean = clean_rut(rut)

    steps.append({
        "title": "Limpieza del RUT",
        "explanation": f"Se eliminan puntos, guiones y espacios → {clean}",
    })

    if len(clean) < 2:
        return build_error(
            error="RUT demasiado corto",
            steps=steps,
        )

    body = clean[:-1]
    dv_input = clean[-1]

    steps.append({
        "title": "Separación cuerpo y dígito verificador",
        "explanation": (
            f"Cuerpo: {body}\n"
            f"DV ingresado: {dv_input}"
        ),
    })

    if not (dv_input.isdigit() or dv_input == "K"):
        return build_error(
            error=f"DV '{dv_input}' no es válido (debe ser 0-9 o K)",
            steps=steps,
        )

    if not body.isdigit():
        return build_error(
            error="El cuerpo del RUT debe contener solo números",
            steps=steps,
        )

    if len(body) != 8:
        return build_error(
            error=f"El cuerpo debe tener exactamente 8 dígitos (tiene {len(body)})",
            steps=steps,
        )

    digits = [int(d) for d in body]
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    reversed_digits = digits[::-1]

    # ── Algoritmo módulo 11 ──────────────────────────────────────

    detail_lines = []

    for i, digit in enumerate(reversed_digits):
        multiplier = multipliers[i % len(multipliers)]
        product = digit * multiplier

        total += product

        detail_lines.append(
            f"{digit} × {multiplier} = {product}"
        )

    steps.append({
        "title": "Algoritmo módulo 11 — productos",
        "explanation": (
            "Se recorre el cuerpo del RUT de derecha a izquierda "
            "multiplicando por el ciclo [2, 3, 4, 5, 6, 7].\n\n"
            + "\n".join(detail_lines)
        ),
    })
    remainder = total % 11
    result = 11 - remainder

    steps.append({
        "title": "Suma total de productos",
        "equation": f"Suma total = {total}",
        "result": str(total),
    })

    steps.append({
        "title": "Resto módulo 11",
        "equation": f"{total} mod 11 = {remainder}",
        "result": str(remainder),
    })

    steps.append({
        "title": "Cálculo del DV esperado",
        "equation": f"11 − {remainder} = {result}",
        "result": str(result),
        "observation": (
            "Si el resultado es 11 → DV = 0\n"
            "Si el resultado es 10 → DV = K"
        ),
    })

    dv_expected = (
        "0"
        if result == 11
        else (
            "K"
            if result == 10
            else str(result)
        )
    )

    steps.append({
        "title": "Comparación de dígitos verificadores",
        "explanation": (
            f"DV esperado: {dv_expected}\n"
            f"DV ingresado: {dv_input}"
        ),
        "result": (
            "Coinciden"
            if dv_expected == dv_input
            else "✗ No coinciden"
        ),
    })

    valid = dv_expected == dv_input
    v = compute_v(dv_input if valid else dv_expected)

    if not valid:
        return build_error(
            error=(
                f"DV incorrecto: ingresó '{dv_input}', "
                f"se esperaba '{dv_expected}'"
            ),
            steps=steps,
            data={
                "clean_rut": clean,
                "body": body,
                "dv_input": dv_input,
                "dv_expected": dv_expected,
            },
        )

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
        },
    )