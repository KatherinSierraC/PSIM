import json

def filtro_rechaza_bandas(fourier_data, low_cutoff, high_cutoff):
    valores = [v.copy() for v in fourier_data]
    N = len(valores)
    
    # Asignar frecuencias correctas
    frequencies = list(range(N))

    # Filtrar frecuencias dentro del rango de rechazo
    for k in range(N):
        if low_cutoff <= abs(frequencies[k]) <= high_cutoff:
            valores[k] = {"real": 0.0, "imag": 0.0}  

    return valores



def lambda_handler(event, context):
    event = json.loads(event) if isinstance(event, str) else event

    fourier_data = event.get("fourier_data", [])
    low_cutoff = event.get("low_cutoff", 5)
    high_cutoff = event.get("high_cutoff", 10)

    resultado = filtro_rechaza_bandas(fourier_data, low_cutoff, high_cutoff)

    return {"filtered_signal": resultado}
