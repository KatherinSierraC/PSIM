import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def cargar_imagen(ruta, redimensionar=(256, 256)):
    """Carga y redimensiona la imagen a escala de grises."""
    img = Image.open(ruta).convert('L')
    if redimensionar:
        img = img.resize(redimensionar)
    return np.array(img)

def añadir_ruido_alta_frecuencia(img, sigma=30, umbral_diff=50):
    """Añade ruido gaussiano solo en bordes/texturas (alta frecuencia)."""
    noisy_img = img.copy()
    h, w = noisy_img.shape
    for x in range(1, h-1):
        for y in range(1, w-1):
            # Detectar bordes (diferencias con vecinos)
            diff = abs(noisy_img[x, y] - np.mean(noisy_img[x-1:x+2, y-1:y+2]))
            if diff > umbral_diff:
                ruido = int(np.random.normal(0, sigma))
                noisy_img[x, y] = np.clip(noisy_img[x, y] + ruido, 0, 255)
    return noisy_img

def aplicar_filtro_disco(img, radio=50 ):
    """Aplica filtro de disco en el dominio de Fourier."""
    fft = np.fft.fftshift(np.fft.fft2(img))
    h, w = img.shape
    Y, X = np.ogrid[:h, :w]
    centro = (h//2, w//2)
    mascara = (X - centro[1])**2 + (Y - centro[0])**2 <= radio**2
    fft_filtrado = fft * mascara
    return np.abs(np.fft.ifft2(np.fft.ifftshift(fft_filtrado))).astype(np.uint8)

# --- Parámetros ajustables ---
ruta_imagen = "eco_bebe.jpg"  
sigma_ruido = 40               # Intensidad del ruido (30-50)
umbral_borde = 15              # Sensibilidad a bordes (10-20)
radio_filtro = 50              # Radio del filtro (20-30)

# --- Proceso completo ---
# 1. Cargar y preparar imagen
original = cargar_imagen(ruta_imagen)

# 2. Añadir ruido en altas frecuencias
img_con_ruido = añadir_ruido_alta_frecuencia(original, sigma=sigma_ruido, umbral_diff=umbral_borde)

# 3. Aplicar filtro de disco
img_filtrada = aplicar_filtro_disco(img_con_ruido, radio=radio_filtro)

# --- Visualización ---
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
axs[0].imshow(original, cmap='gray')
axs[0].set_title("Original")
axs[0].axis('off')

axs[1].imshow(img_con_ruido, cmap='gray')
axs[1].set_title(f"Con ruido (σ={sigma_ruido})")
axs[1].axis('off')

axs[2].imshow(img_filtrada, cmap='gray')
axs[2].set_title(f"Filtrada (radio={radio_filtro})")
axs[2].axis('off')

plt.tight_layout()
plt.show()