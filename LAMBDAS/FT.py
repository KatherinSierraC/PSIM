import numpy as np
import matplotlib.pyplot as plt

def TF(señal):
    N = len(señal)
    valores = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            valores[k] += señal[n] * np.exp(-2j * np.pi * k * n / N)
    freq = np.arange(N)
    return freq, valores

def Graficar_señales_TF(señal, freq, valores):
    plt.figure(figsize=(12, 8))
    
    # Plot original signal
    plt.subplot(3, 1, 1)
    plt.plot(señal, label='Señal original')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.title('Señal en el dominio del tiempo')
    plt.legend()
    
    # Plot DFT Magnitude
    plt.subplot(3, 1, 2)
    plt.plot(freq[:len(freq)//2], np.abs(valores[:len(freq)//2]), label='Magnitud DFT')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud')
    plt.title('Magnitud de la Transformada de Fourier Discreta (DFT)')
    plt.legend()
    
    # Plot DFT Phase
    plt.subplot(3, 1, 3)
    plt.plot(freq[:len(freq)//2], np.angle(valores[:len(freq)//2]), label='Fase DFT')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Fase [radianes]')
    plt.title('Fase de la Transformada de Fourier Discreta (DFT)')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Señal de entrada (se asume que ya está definida)
señal = np.array([1,2,3,1,1,2])  # Reemplazar con la señal real

# Calcular DFT
freq, datos = TF(señal)

# Graficar señal, magnitud y fase de la DFT
Graficar_señales_TF(señal, freq, datos)
