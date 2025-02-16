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
    return filtered_signal, valores, frequencies