import json

def filtro_pasa_bajas(fourier_data, cutoff):
    print(f"Datos recibidos en filtro: {json.dumps(fourier_data)}")  # 🛠 Log de entrada
    valores = fourier_data[:]  # Copia la lista para evitar modificar la original
    N = len(valores)

    if N == 0:
        print(" Advertencia: Lista de Fourier vacía en filtro")  # 🛠 Log de advertencia
        return valores  

    # Calcular las frecuencias adecuadas
    frequencies = list(range(N))

    # Filtrar frecuencias altas
    for k in range(N):
        if abs(frequencies[k]) > cutoff:
            valores[k]["real"] = 0  
            valores[k]["imag"] = 0  

    print(f"Datos después del filtro: {json.dumps(valores)}")  # 🛠 Log de salida
    return valores

def lambda_handler(event, context):
    try:
        print(f"Evento recibido en filtro pasa-bajas: {json.dumps(event)}")  # Log de entrada

        fourier_data = event.get("fourier_data", [])
        cutoff = event.get("cutoff", 10)

        if not isinstance(fourier_data, list) or not all(isinstance(x, dict) and "real" in x and "imag" in x for x in fourier_data):
            raise ValueError(f"Formato de 'fourier_data' incorrecto: {fourier_data}")

        resultado = filtro_pasa_bajas(fourier_data, cutoff)

        print(f"Señal filtrada generada: {json.dumps(resultado)}")  # Log de salida

        return {"filtered_signal": resultado}  

    except Exception as e:
        print(f" Error en filtro pasa-bajas: {str(e)}")  # Log del error
        return {"error": str(e)}
