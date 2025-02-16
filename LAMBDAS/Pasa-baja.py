import math
import matplotlib.pyplot as plt
import numpy as np

def TF(señal):
                            #FUNCION LAMBDA DE TRANSFORMADA DE FOURIER 
    N = len(señal)
    valores = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            valores[k] += señal[n] * np.exp(-2j * np.pi * k * n / N)
    freq = np.fft.fftfreq(N, d=1/1000)  # Frecuencias reales en Hz
    return freq, valores

def IFT(valores):
                                ##transformada inversa de fourier (LAMBDA)
    N = len(valores)
    señal_reconstruida = np.zeros(N, dtype=complex)
    for n in range(N):
        for k in range(N):
            señal_reconstruida[n] += valores[k] * np.exp(2j * np.pi * k * n / N)  # SIGNO CORREGIDO
        señal_reconstruida[n] /= N  # Normalización
    return señal_reconstruida.real  # Solo parte real

def pasabajas(signal, cutoff, sampling_rate=1000):
      ####FILTROO##
    N = len(signal)
    frequencies, valores = TF(signal)  # Obtener la DFT
    
    
    for k in range(N):
        if abs(frequencies[k]) > cutoff:
            valores[k] = 0  # ELIMINA  FRECUENCIAS ALTAS


    filtered_signal = IFT(valores)  
    return filtered_signal, valores, frequencies  # Devuelve la señal filtrada y la DFT modificada

# Parámetros 
sampling_rate = 1000  
N = 100  # muestras 
t = np.arange(N) / sampling_rate  # Vector de tiempo

# Señal original ejemplo 
signal = (
    np.sin(2 * np.pi * 10 * t)  # Componente de 10 Hz
    + 0.5 * np.sin(2 * np.pi * 50 * t)  # Componente de 50 Hz
    + 0.3 * np.sin(2 * np.pi * 120 * t)  # Componente de 120 Hz
)


cutoff = 30
filtered_signal, valores_filtrados, frequencies = pasabajas(signal, cutoff, sampling_rate)

# Calcular la DFT de la señal original
freq_original, valores_original = TF(signal)

# Magnitud de la DFT (espectro)
magnitude_original = np.abs(valores_original)
magnitude_filtered = np.abs(valores_filtrados)

# Graficar resultados
plt.figure(figsize=(12, 8))

# Señal original
plt.subplot(3, 1, 1)
plt.plot(t, signal, label="Señal Original", color="blue")
plt.title("Señal Original en el Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

# Señal filtrada
plt.subplot(3, 1, 2)
plt.plot(t, filtered_signal, label="Señal Filtrada", color="green")
plt.title("Señal Filtrada en el Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

# Espectro de frecuencia
plt.subplot(3, 1, 3)
plt.plot(frequencies, magnitude_original, label="DFT Señal Original", color="orange")
plt.plot(frequencies, magnitude_filtered, label="DFT Señal Filtrada", color="red", alpha=0.7)
plt.title("Transformada de Fourier")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.xlim(0, 200)  # Limitar el eje x para mejor visualización
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
