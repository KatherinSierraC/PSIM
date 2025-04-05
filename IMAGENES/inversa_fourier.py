import numpy as np
from PIL import Image
import traceback

def cargar_imagen_a_matriz(ruta_imagen, redimensionar=None):
    """Carga una imagen y la convierte a matriz NumPy, opcionalmente redimensiona."""
    try:
        imagen = Image.open(ruta_imagen).convert("L")
        if redimensionar:
            imagen = imagen.resize(redimensionar)
        return np.array(imagen, dtype=np.float64)  # Convertir a matriz NumPy
    except FileNotFoundError:
        print(f"⚠️ ERROR: No se encontró la imagen en '{ruta_imagen}'.")
        return None
    
    
def TF_2D_numpy(imagen_en_fourier):
    """Transformada de Fourier 2D usando NumPy (rápido)."""
    return np.fft.fft2(imagen_en_fourier)

############DE FRECUENCIA A TIEMPO #################
def IDFT_2D_numpy(imagen_frec):
    """Transformada Inversa de Fourier 2D usando NumPy."""
    return np.fft.ifft2(imagen_frec)
###########RECONSTRUYE LA IMAGEN VISIBLE ###
def reconstruir_imagen_numpy(matriz_compleja):
    """Reconstruye la imagen a partir de la matriz compleja."""
    # Tomar magnitud y normalizar a 0-255
    magnitud = np.abs(matriz_compleja)
    imagen_normalizada = (magnitud - np.min(magnitud)) / (np.max(magnitud) - np.min(magnitud)) * 255
    return Image.fromarray(imagen_normalizada.astype(np.uint8))

if __name__ == "__main__":
    try:
        print("═"*50)
        print("Iniciando proceso de transformada de Fourier".center(50))
        print("═"*50)
        
        # 1. Cargar imagen (opcional: redimensionar para mayor velocidad)
        ruta = "eco_bebe.jpg"
        print(f"\nBuscando imagen en: {ruta}")
        imagen_matriz = cargar_imagen_a_matriz(ruta, redimensionar=(256, 256))  # Reducción opcional
        
        if imagen_matriz is None:
            print("\n❌ Error: No se pudo cargar la imagen.")
            input("Presiona Enter para salir...")
            exit()
        
        print(f"\n✔ Imagen cargada ({imagen_matriz.shape[1]}x{imagen_matriz.shape[0]} píxeles)")
        
        # 2. Transformada de Fourier (¡Ahora es instantáneo!)
        print("\nCalculando Transformada de Fourier 2D con NumPy...")
        tf_resultado = TF_2D_numpy(imagen_matriz)
        print("✔ Transformada completada en milisegundos")
        
        # 3. Transformada Inversa
        print("\nCalculando Transformada Inversa...")
        imagen_reconstruida_compleja = IDFT_2D_numpy(tf_resultado)
        print("✔ Transformada inversa completada")
        
        # 4. Reconstrucción
        print("\nReconstruyendo imagen...")
        imagen_reconstruida = reconstruir_imagen_numpy(imagen_reconstruida_compleja)
        
        # 5. Guardar resultado
        output_path = "reconstruida_numpy.jpg"
        imagen_reconstruida.save(output_path)
        print(f"\n✅ ¡Éxito! Imagen reconstruida guardada como '{output_path}'")
        print("═"*50)
        input("Presiona Enter para finalizar...")
        
    except Exception as e:
        print("\n❌ Error inesperado:")
        traceback.print_exc()
        input("Presiona Enter para salir...")