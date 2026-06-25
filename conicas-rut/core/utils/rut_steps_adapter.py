# conicas-rut/core/utils/rut_steps_adapter.py

import re


def parse_rut_steps(result: dict) -> list[dict]:
    """
    Convierte los pasos planos generados por validate_rut() en una estructura
    más clara para mostrarlos en la interfaz.
    """
    raw: list[str] = result.get("steps", [])
    data: dict = result.get("data", {})
    is_valid = result.get("valid", False)

    structured: list[dict] = []

    for line in raw:
        if line.startswith("RUT limpio:"):
            clean = line.split(":", 1)[-1].strip()
            structured.append({
                "title": "Limpieza del RUT",
                "explanation": (
                    "Se eliminan puntos, guiones y espacios. "
                    "El dígito verificador se convierte a mayúscula."
                ),
                "equation": f"RUT limpio → {clean}",
            })

        elif line.startswith("Proceso módulo 11"):
            structured.append({
                "title": "Algoritmo módulo 11",
                "explanation": (
                    "Se recorre el cuerpo del RUT de derecha a izquierda, "
                    "multiplicando cada dígito por el ciclo [2, 3, 4, 5, 6, 7]."
                ),
            })

        elif re.fullmatch(r"\d+ × \d+ = \d+", line):
            digit, multiplier, product = re.findall(r"\d+", line)
            structured.append({
                "title": f"Dígito {digit}",
                "explanation": None,
                "equation": f"{digit} × {multiplier} = {product}",
                "result": product,
            })

        elif line.startswith("Suma total"):
            total = line.split("=")[-1].strip()
            structured.append({
                "title": "Suma total de productos",
                "explanation": "Suma acumulada de todos los productos anteriores.",
                "equation": line,
                "result": total,
            })

        elif "% 11" in line:
            remainder = line.split("=")[-1].strip()
            structured.append({
                "title": "Resto módulo 11",
                "explanation": "Se calcula el resto de dividir la suma total entre 11.",
                "equation": line,
                "result": remainder,
            })

        elif line.startswith("11 -"):
            result_value = line.split("=")[-1].strip()

            observation = None
            if result_value == "11":
                observation = "Resultado 11 → DV = 0"
            elif result_value == "10":
                observation = "Resultado 10 → DV = K"

            structured.append({
                "title": "Cálculo del DV esperado",
                "explanation": "Se resta el resto a 11 para obtener el dígito verificador esperado.",
                "equation": line,
                "result": result_value,
                "observation": observation,
            })

        elif line.startswith("DV esperado"):
            dv_expected = line.split("=")[-1].strip()
            structured.append({
                "title": "DV esperado",
                "explanation": None,
                "result": dv_expected,
            })

        elif line.startswith("DV ingresado"):
            dv_input = line.split("=")[-1].strip()
            dv_expected = data.get("dv_expected", "?")
            v = data.get("v")

            if is_valid:
                result_text = "Coinciden — RUT válido"
                observation = f"Variable auxiliar v = {v}" if v is not None else None
            else:
                result_text = "No coinciden — RUT inválido"
                observation = None

            structured.append({
                "title": "Verificación del DV",
                "explanation": "Se compara el DV ingresado con el DV calculado.",
                "equation": f"ingresado '{dv_input}' = esperado '{dv_expected}'",
                "result": result_text,
                "observation": observation,
            })

    return structured