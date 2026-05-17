from tramo_function import CrearVariables

def CrearTablaValores(a, funcion):
    deltas_izq = [-1, -0.1, -0.01, -0.001]
    deltas_der = [0.001, 0.01, 0.1, 1]
    
    tabla_izq = []
    for delta in deltas_izq:
        x = a + delta
        y = funcion(x)
        tabla_izq.append({"x": x, "y": y})
        
    tabla_der = []
    for delta in deltas_der:
        x = a + delta
        y = funcion(x)
        tabla_der.append({"x": x, "y": y})
        
    return {"izquierda": tabla_izq, "derecha": tabla_der}

datos_tramo = CrearVariables("218992234") # adivina el rut

funcion_evaluar = datos_tramo["funcion"]
punto_critico = datos_tramo["a"]

tabla_final = CrearTablaValores(punto_critico, funcion_evaluar)

print(tabla_final)