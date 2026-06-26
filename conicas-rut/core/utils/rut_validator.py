# conicas-rut/core/utils/rut_validator.py

from core.utils.result_models import build_success, build_error

def clean_rut(rut: str) -> str:
    # Aqui limpiamos el rut pa que no tenga puntos ni guiones, puro texto
    return (
        rut.replace(".", "")
           .replace("-", "")
           .replace(" ", "")
           .upper()
    )

def compute_v(dv: str) -> int:
    # Sacamos la variable v segun la rubrica para usarla despues en los coeficientes
    if dv == "K":
        return 10
    if dv == "0":
        return 11
    if dv.isdigit():
        return int(dv)
    return -1

def validate_rut(rut: str) -> dict:
    # Esta funcion valida el rut con el modulo 11 y guarda los pasos para mostrarlos en la UI
    steps: list[str] = []

    if not rut or not isinstance(rut, str):
        return build_error(error="RUT vacio o tipo invalido")

    clean = clean_rut(rut)
    steps.append(f"RUT limpio: {clean}")

    if len(clean) < 2:
        return build_error(
            error="RUT demaciado corto",
            steps=steps,
        )

    body = clean[:-1]
    dv_input = clean[-1]

    if not (dv_input.isdigit() or dv_input == "K"):
        return build_error(
            error=f"DV '{dv_input}' no es valido. Debe ser 0-9 o K.",
            steps=steps,
        )

    if not body.isdigit():
        return build_error(
            error="El cuerpo del RUT debe tener puros numeros.",
            steps=steps,
        )

    if len(body) != 8:
        return build_error(
            error=f"El cuerpo debe tener 8 digitos. Tiene {len(body)}.",
            steps=steps,
        )

    digits = [int(digit) for digit in body]

    # La multiplicacion de los digitos se hace de derecha a izq
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    multiplier_index = 0

    steps.append("Proceso modulo 11:")

    for digit in digits[::-1]:
        multiplier = multipliers[multiplier_index % len(multipliers)]
        product = digit * multiplier
        total += product
        steps.append(f"{digit} × {multiplier} = {product}")
        multiplier_index += 1

    # Calculo del resto
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
            error=f"DV incorrecto: ingreso '{dv_input}', se esperaba '{dv_expected}'.",
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
        explanation="El RUT es valido.",
        steps=steps,
        data={
            "clean_rut": clean,
            "body": body,
            "digits": digits,
            "named_digits": {
                f"d{i + 1}": digits[i]
                for i in range(8)
            },
            "dv_input": dv_input,
            "dv_expected": dv_expected,
            "v": v,
        },
    )