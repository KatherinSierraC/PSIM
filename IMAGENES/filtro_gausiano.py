import numpy as np
import random
import math
from PIL import Image
import traceback

############# CARGA IMAGEN Y LA CONVIERTE EN MATRIZ NUMPY ESCALA DE GRISES #############
def cargar_imagen_a_matriz(ruta_imagen, redimensionar=None):
    try:
        imagen = Image.open(ruta_imagen).convert("L")
        if redimensionar:
            imagen = imagen.resize(redimensionar)
        return np.array(imagen, dtype=np.float64)
    except FileNotFoundError:
        print(f"⚠️ ERROR: No se encontró la imagen en '{ruta_imagen}'.")
        return None

############# AÑADIR RUIDO GAUSSIANO ################
def añadir_ruido_gaussiano(imagen_np, media=0, sigma=10):
    ruido = np.random.normal(media, sigma, imagen_np.shape)
    imagen_ruido = np.clip(imagen_np + ruido, 0, 255)
    return imagen_ruido

############# TRANSFORMADA DE FOURIER 2D ###########
def TF_2D_numpy(imagen):
    return np.fft.fft2(imagen)

############# TRANSFORMADA INVERSA #################
def IDFT_2D_numpy(imagen_frec):
    return np.fft.ifft2(imagen_frec)

############# RECONSTRUCCIÓN IMAGEN 0-255 ###########
def reconstruir_imagen_numpy(matriz_compleja):
    magnitud = np.abs(matriz_compleja)
    imagen_normalizada = (magnitud - np.min(magnitud)) / (np.max(magnitud) - np.min(magnitud)) * 255
    return Image.fromarray(imagen_normalizada.astype(np.uint8))

############# CREAR FILTRO GAUSSIANO 2D ############
def crear_filtro_gaussiano(ancho, alto, sigma):
    filtro = [[0.0 for _ in range(ancho)] for _ in range(alto)]
    cx, cy = ancho // 2, alto // 2

    for y in range(alto):
        for x in range(ancho):
            dx = x - cx
            dy = y - cy
            filtro[y][x] = math.exp(-(dx**2 + dy**2) / (2 * sigma**2))
    
    return filtro

############# APLICAR FILTRO A COMPONENTES FRECUENCIALES ##########
def aplicar_filtro_frecuencia(fft_real, fft_imag, filtro):
    alto = len(fft_real)
    ancho = len(fft_real[0])
    
    resultado_real = [[0.0 for _ in range(ancho)] for _ in range(alto)]
    resultado_imag = [[0.0 for _ in range(ancho)] for _ in range(alto)]

    for y in range(alto):
        for x in range(ancho):
            h = filtro[y][x]
            resultado_real[y][x] = fft_real[y][x] * h
            resultado_imag[y][x] = fft_imag[y][x] * h

    return resultado_real, resultado_imag

############# PROGRAMA PRINCIPAL ####################
if __name__ == "__main__":
    try:
        print("═" * 50)
        print("Inicio del proceso de procesamiento de imagen".center(50))
        print("═" * 50)

        # 1. Cargar imagen
        ruta = "eco_bebe.jpg"
        print(f"\nCargando imagen desde: {ruta}")
        imagen_matriz = cargar_imagen_a_matriz(ruta, redimensionar=(256, 256))

        if imagen_matriz is None:
            print("\n❌ No se pudo cargar la imagen.")
            input("Presiona Enter para salir...")
            exit()

        print(f"\n✔ Imagen cargada ({imagen_matriz.shape[1]}x{imagen_matriz.shape[0]})")

        # 2. Añadir ruido gaussiano
        print("\nAñadiendo ruido gaussiano...")
        imagen_con_ruido = añadir_ruido_gaussiano(imagen_matriz, media=0, sigma=20)
        Image.fromarray(imagen_con_ruido.astype(np.uint8)).save("imagen_con_ruido.jpg")
        print("✔ Ruido añadido y guardado como 'imagen_con_ruido.jpg'")

        # 3. Transformada de Fourier
        print("\nAplicando Transformada de Fourier...")
        tf_resultado = TF_2D_numpy(imagen_con_ruido)
        tf_real = tf_resultado.real
        tf_imag = tf_resultado.imag
        print("✔ Transformada completada")

        # 4. Crear y aplicar filtro gaussiano
        print("\nCreando filtro gaussiano en frecuencia...")
        filtro = crear_filtro_gaussiano(imagen_matriz.shape[1], imagen_matriz.shape[0], sigma=10)
        print("Aplicando filtro gaussiano...")
        tf_real_filtrado, tf_imag_filtrado = aplicar_filtro_frecuencia(tf_real, tf_imag, filtro)
        tf_filtrado_complejo = np.array(tf_real_filtrado) + 1j * np.array(tf_imag_filtrado)
        print("✔ Filtro aplicado")

        # 5. Transformada Inversa
        print("\nRealizando transformada inversa para reconstrucción...")
        imagen_reconstruida_compleja = IDFT_2D_numpy(tf_filtrado_complejo)
        imagen_reconstruida = reconstruir_imagen_numpy(imagen_reconstruida_compleja)
        imagen_reconstruida.save("imagen_filtrada.jpg")
        print("✔ Imagen filtrada reconstruida y guardada como 'imagen_filtrada.jpg'")

        print("\n✅ Proceso completado exitosamente")
        print("═" * 50)
        input("Presiona Enter para finalizar...")

    except Exception as e:
        print("\n❌ Error inesperado:")
        traceback.print_exc()
        input("Presiona Enter para salir...")
