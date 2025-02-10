#Tranformada Inversa de Furier

import numpy as np
import matplotlib.pyplot as plt

def IFT(valores):
    N = len(valores)
    señal_reconstruida = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            señal_reconstruida[k] += valores[k] * np.exp(-2j * np.pi * k * n / N)
        señal_reconstruida[k] /= N
    freq = np.arange(N)
    return señal_reconstruida.real

def Graficar_señal_reconstruida(señal_reconstruida):
    plt.figure(figsize=(8, 4))
    plt.plot(señal_reconstruida, label='Señal reconstruida')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.title('Señal recostruida IFT')
    plt.legend()

    plt.show()
    
# Datos para realizar la Transfomada Inversa de Furier
valores = np.array([1 + 1j * (2/3), 2 - 1j * (3/2), 3, 1, 1, 2]) 

# Se calcula la Transformada Inversa de Furier
señal_tiempo = IFT(valores)

# Graficar señal reconstruida
Graficar_señal_reconstruida(señal_tiempo)
