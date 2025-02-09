import numpy as np
import matplotlib.pyplot as plt

def senal(a=2, periodo=12, n0=1, muestras=14):
    w = 2 * np.pi / periodo  # Frecuencia angular
    ni = np.arange(n0, n0 + muestras, 1)
    fx = lambda n: a * np.sin(w * (n - n0))  # Corrige el desfase
    senal = fx(ni)
    return ni, senal

# Trans
ni, senal = senal()
transformada = np.fft.fft(senal)
tm = np.abs(transformada)
tfase = np.angle(transformada)

# Transformada inversa 
inversa = np.fft.ifft(transformada)

plt.figure(figsize=(12, 8))

# Gráfica 1: Señal x[n]
plt.subplot(4, 1, 1)
plt.stem(ni, senal, basefmt=" ")
plt.title("Señal x[n]")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid()

# Gráfico de la magnitud
plt.subplot(4, 1, 2)
plt.plot(ni, tm, '.-')
plt.title('Magnitud de la Transformada de Fourier')
plt.xlabel('Índice')
plt.ylabel('Magnitud')
plt.grid()

# Gráfico de la fase
plt.subplot(4, 1, 3)
plt.plot(ni, tfase, '.-')
plt.title('Fase de la Transformada de Fourier')
plt.xlabel('Índice')
plt.ylabel('Fase (radianes)')
plt.grid()

# Gráfica 4: inversa
plt.subplot(4, 1, 4)
plt.stem(ni, inversa.real, basefmt=" ")  
plt.title("Señal Reconstruida (Transformada Inversa)")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.tight_layout()  #
plt.show()