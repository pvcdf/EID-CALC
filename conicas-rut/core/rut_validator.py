


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

    body = clean[:-1]
    dv_input = clean[-1]

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

    digits = [int(d) for d in body]

    # Algoritmo módulo 11
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    multiplier_index = 0
    reversed_digits = digits[::-1]

    steps.append("Proceso módulo 11:")
    for digit in reversed_digits:
        multiplier = multipliers[multiplier_index % len(multipliers)]
        product = digit * multiplier
        total += product
        steps.append(f"  {digit} × {multiplier} = {product}")
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

    valid = dv_expected == dv_input

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
