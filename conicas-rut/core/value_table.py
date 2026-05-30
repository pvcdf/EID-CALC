#conicas-rut/core/value_table.py

from core.tramo_function import CrearVariables

def CrearTablaValores(a, funcion):
    deltas_izq = [-1, -0.1, -0.01, -0.001]
    deltas_der = [0.001, 0.01, 0.1, 1]
    
    tabla_izq = []
    for delta in deltas_izq:
        x = a + delta
        try:
            y = funcion(x)
        except ZeroDivisionError:
            y = None
        tabla_izq.append({"x": x, "y": y})
        
    tabla_der = []
    for delta in deltas_der:
        x = a + delta
        try:
            y = funcion(x)
        except ZeroDivisionError:
            y = None
        tabla_der.append({"x": x, "y": y})
        
    return {"izquierda": tabla_izq, "derecha": tabla_der}
