import math
import matplotlib.pyplot as plt

def TF(señal):
    N = len(señal)
    valores = [0] * N
    for k in range(N):
        real = 0
        imag = 0
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            real += señal[n] * math.cos(angle)
            imag += señal[n] * math.sin(angle)
        valores[k] = complex(real, imag)
    freq = list(range(N))
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
    magnitudes = [math.sqrt(v.real**2 + v.imag**2) for v in valores]
    plt.plot(freq[:len(freq)//2], magnitudes[:len(freq)//2], label='Magnitud DFT')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud')
    plt.title('Magnitud de la Transformada de Fourier Discreta (DFT)')
    plt.legend()
    
    # Plot DFT Phase
    fases = [math.atan2(v.imag, v.real) for v in valores]
    plt.subplot(3, 1, 3)
    plt.plot(freq[:len(freq)//2], fases[:len(freq)//2], label='Fase DFT')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Fase [radianes]')
    plt.title('Fase de la Transformada de Fourier Discreta (DFT)')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Señal de entrada
señal = [1, 2, 3, 1, 1, 2]  # Reemplazar con la señal real

# Calcular DFT
freq, datos = TF(señal)

# Graficar señal, magnitud y fase de la DFT
Graficar_señales_TF(señal, freq, datos)
