# Transformada Inversa de Fourier
import math
import matplotlib.pyplot as plt

def IFT(valores):
    N = len(valores)
    señal_reconstruida = [0] * N  # Lista de ceros para almacenar la señal reconstruida

    for k in range(N):
        suma = 0
        for n in range(N):
            angulo = 2 * math.pi * k * n / N
            suma += valores[n].real * math.cos(angulo) - valores[n].imag * math.sin(angulo) \
                  + 1j * (valores[n].real * math.sin(angulo) + valores[n].imag * math.cos(angulo))
        señal_reconstruida[k] = suma / N  # Normalización

    return [x.real for x in señal_reconstruida]  # Solo parte real

def Graficar_señal_reconstruida(señal_reconstruida):
    plt.figure(figsize=(8, 4))
    plt.plot(señal_reconstruida, label='Señal reconstruida')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.title('Señal reconstruida IFT')
    plt.legend()
    plt.show()

# Datos para realizar la Transformada Inversa de Fourier
valores = [
    complex(1, 2/3), 
    complex(2, -3/2), 
    complex(3, 0), 
    complex(1, 0), 
    complex(1, 0), 
    complex(2, 0)
]

# Se calcula la Transformada Inversa de Fourier
señal_tiempo = IFT(valores)

# Graficar señal reconstruida
Graficar_señal_reconstruida(señal_tiempo)
