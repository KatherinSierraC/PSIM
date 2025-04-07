import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Función para cargar imagen y convertir a escala de grises
def cargar_imagen_grises(ruta):
    imagen = Image.open(ruta).convert('L')  # Convertir a escala de grises
    return np.array(imagen, dtype=float)

# Función para aplicar convolución 2D manual
def convolucion2d(imagen, kernel):
    alto, ancho = imagen.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Padding
    imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    resultado = np.zeros_like(imagen)

    for i in range(alto):
        for j in range(ancho):
            region = imagen_padded[i:i+kh, j:j+kw]
            resultado[i, j] = np.sum(region * kernel)
    
    return resultado

# Kernels Sobel
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

sobel_y = np.array([[-1, -2, -1],
                    [ 0,  0,  0],
                    [ 1,  2,  1]])

# Cargar imagen
imagen = cargar_imagen_grises('C:\\Users\\Usuario\\Desktop\\Universidad\\PSIM\\PSIM-1\\IMAGENES\\eco_bebe.jpg')

# Aplicar Sobel
grad_x = convolucion2d(imagen, sobel_x)
grad_y = convolucion2d(imagen, sobel_y)

# Mostrar resultados
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.title('Sobel X')
plt.imshow(np.abs(grad_x), cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Sobel Y')
plt.imshow(np.abs(grad_y), cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()