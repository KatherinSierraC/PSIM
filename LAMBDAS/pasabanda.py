import json

def filtro_pasa_banda(fourier_data, low_cutoff, high_cutoff):    
    if not isinstance(fourier_data, list) or not fourier_data:
        return []  # Retorna lista vacía si los datos no son válidos

    valores = [v.copy() for v in fourier_data]
    N = len(valores)
    
    # Asignar frecuencias correctas considerando simetría
    frequencies = [(k if k < N // 2 else k - N) for k in range(N)]

    # Filtrar frecuencias fuera del rango de paso
    for k in range(N):
        if not (low_cutoff <= abs(frequencies[k]) <= high_cutoff):
            valores[k] = {"real": 0.0, "imag": 0.0}  # Pone en cero las frecuencias fuera del rango

    return valores  

def lambda_handler(event, context):
    # AWS Lambda ya recibe `event` como diccionario, no es necesario `json.loads(event)`
    fourier_data = event.get("fourier_data", [])
    low_cutoff = event.get("low_cutoff", 5)
    high_cutoff = event.get("high_cutoff", 10)

    resultado = filtro_pasa_banda(fourier_data, low_cutoff, high_cutoff)

    return {"filtered_signal": resultado}
