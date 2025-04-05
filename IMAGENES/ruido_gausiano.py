from PIL import Image
import random
import numpy as np

def cargar_imagen_grises(ruta):
    """Carga la imagen y la convierte a escala de grises."""
    img = Image.open(ruta).convert("L")
    return img

def añadir_ruido_gaussiano_alta_frecuencia(img, sigma=25, umbral_borde=30):
   
    pixeles = img.load()
    ancho, alto = img.size
    
    for x in range(ancho):
        for y in range(alto):
            # Solo añade ruido en píxeles de alta frecuencia (bordes)
            if x > 0 and y > 0 and x < ancho-1 and y < alto-1:
                # Calcular diferencia promedio con 4 vecinos
                vecinos = [
                    pixeles[x-1, y], pixeles[x+1, y],
                    pixeles[x, y-1], pixeles[x, y+1]
                ]
                diff = abs(pixeles[x, y] - sum(vecinos) // 4)
                
                # Si es un borde (alta frecuencia), añade ruido
                if diff > umbral_borde:
                    ruido = int(random.gauss(0, sigma))
                    nuevo_valor = max(0, min(255, pixeles[x, y] + ruido))
                    pixeles[x, y] = nuevo_valor
    
    return img

# --- Ejemplo de uso ---
imagen_original = cargar_imagen_grises("foto_prueba.jpg")
imagen_con_ruido = añadir_ruido_gaussiano_alta_frecuencia(
    imagen_original.copy(),
    sigma=100,       # Intensidad del ruido
    umbral_borde=20  # Ajusta para detectar más/menos bordes
)
imagen_con_ruido.save("imagen_con_ruido_alta_frecuencia.jpg")