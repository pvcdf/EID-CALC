"""
Validador de RUT chileno - Algoritmo Módulo 11
Ref: https://es.wikipedia.org/wiki/Rol_%C3%9Anico_Tributario
"""

import re


def calculate_check_digit(rut_number: str) -> str:
    """
    Calcula el dígito verificador usando el algoritmo Módulo 11.
    
    Args:
        rut_number: String con solo dígitos (ej: "30686957")
    
    Returns:
        String con el dígito verificador (0-9 o K)
    """
    # Asegurar que solo tenemos dígitos
    rut_clean = re.sub(r'\D', '', str(rut_number))
    
    if not rut_clean or not rut_clean.isdigit():
        return None
    
    # Multiplicadores: 2, 3, 4, 5, 6, 7, 2, 3, ...
    multipliers = [2, 3, 4, 5, 6, 7]
    
    # Procesar de derecha a izquierda
    total = 0
    for i, digit in enumerate(reversed(rut_clean)):
        multiplier = multipliers[i % 6]
        total += int(digit) * multiplier
    
    # Calcular remainder
    remainder = total % 11
    
    # Restar de 11
    check_digit = 11 - remainder
    
    # Convertir a la representación correcta
    if check_digit == 11:
        return "0"
    elif check_digit == 10:
        return "K"
    else:
        return str(check_digit)


def validate_rut(rut_input: str) -> dict:
    """
    Valida un RUT chileno.
    
    Args:
        rut_input: String en formato XX.XXX.XXX-X o XXXXXXXX-X o variaciones
    
    Returns:
        dict con:
            - "valid": bool
            - "rut_clean": str (ej: "30686957-4")
            - "rut_formatted": str (ej: "30.686.957-4")
            - "error": str (descripción del error si aplica)
    """
    result = {
        "valid": False,
        "rut_clean": None,
        "rut_formatted": None,
        "error": None,
    }
    
    if not rut_input or not isinstance(rut_input, str):
        result["error"] = "RUT vacío o inválido"
        return result
    
    # Limpiar: remover espacios, puntos
    rut_cleaned = rut_input.strip().replace(".", "").replace(" ", "").upper()
    
    # Debe tener formato XXXXX-X (mínimo)
    if "-" not in rut_cleaned:
        result["error"] = "RUT debe incluir guion (ej: 12345678-9)"
        return result
    
    parts = rut_cleaned.split("-")
    if len(parts) != 2:
        result["error"] = "Formato inválido: debe ser XXX.XXX.XXX-X"
        return result
    
    rut_number, provided_digit = parts[0], parts[1].strip()
    
    # Validar que rut_number sea solo dígitos
    if not rut_number.isdigit():
        result["error"] = "RUT debe contener solo dígitos"
        return result
    
    # Validar que provided_digit sea dígito o K
    if not (provided_digit.isdigit() or provided_digit == "K"):
        result["error"] = "Dígito verificador debe ser 0-9 o K"
        return result
    
    # Validar rango de RUT (Chile: aprox. 3.000.000 a 27.000.000+)
    # Se permite rango más amplio para futuras actualizaciones
    rut_num_int = int(rut_number)
    if rut_num_int < 100000:  # Mínimo muy bajo para aceptar RUTs antiguos
        result["error"] = "RUT fuera de rango válido (muy bajo)"
        return result
    
    # Calcular dígito correcto
    correct_digit = calculate_check_digit(rut_number)
    
    if correct_digit is None:
        result["error"] = "No se pudo calcular dígito verificador"
        return result
    
    # Comparar
    if provided_digit != correct_digit:
        result["error"] = f"Dígito verificador incorrecto (debería ser {correct_digit})"
        return result
    
    # Éxito
    result["valid"] = True
    result["rut_clean"] = f"{rut_number}-{provided_digit}"
    
    # Formatear con puntos
    if len(rut_number) >= 8:
        formatted = f"{rut_number[:-6]}.{rut_number[-6:-3]}.{rut_number[-3:]}-{provided_digit}"
    else:
        formatted = f"{rut_number}-{provided_digit}"
    result["rut_formatted"] = formatted
    
    return result


# Tests básicos
if __name__ == "__main__":
    # Ejemplos que deberían pasar
    test_cases = [
        ("30.686.957-4", True),
        ("30686957-4", True),
        ("30686957-5", False),
        ("1.234.567-K", True),
        ("12345670-K", True),
        ("invalid", False),
        ("", False),
    ]
    
    for rut, should_pass in test_cases:
        result = validate_rut(rut)
        print(f"{rut:20} → Valid: {result['valid']:5} | {result.get('error', 'OK')}")
