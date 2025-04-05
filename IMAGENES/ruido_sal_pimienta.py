import random
from PIL import Image

def agregar_ruido_sal_y_pimienta(imagen_matriz, porcentaje_ruido):
    """Agrega ruido de sal y pimienta a una imagen en formato de matriz 2D."""
    alto = len(imagen_matriz)
    ancho = len(imagen_matriz[0])
    
    # Número total de píxeles en la imagen
    total_pixeles = alto * ancho
    
    # Número de píxeles que serán modificados con ruido (según el porcentaje)
    num_ruido = int(total_pixeles * porcentaje_ruido / 100)
    
    for _ in range(num_ruido):
        # Seleccionar un píxel aleatorio
        y = random.randint(0, alto - 1)
        x = random.randint(0, ancho - 1)
        
        # Decidir si poner "sal" (255) o "pimienta" (0)
        if random.random() < 0.5:
            imagen_matriz[y][x] = 255  # Sal
        else:
            imagen_matriz[y][x] = 0    # Pimienta
    
    return imagen_matriz

def cargar_imagen_a_matriz(ruta_imagen):
    """Carga una imagen JPEG y la convierte en una matriz 2D de escala de grises."""
    imagen = Image.open(ruta_imagen).convert("L")  # Convertir a escala de grises
    ancho, alto = imagen.size
    
    # Convertir la imagen en una matriz 2D de píxeles
    matriz = [[imagen.getpixel((x, y)) for x in range(ancho)] for y in range(alto)]
    
    return matriz

def guardar_imagen(matriz_2d, nombre_archivo):
    """Guarda una imagen 2D a partir de una matriz de píxeles."""
    alto = len(matriz_2d)
    ancho = len(matriz_2d[0])
    
    imagen = Image.new("L", (ancho, alto))  # "L" significa escala de grises
    for y in range(alto):
        for x in range(ancho):
            imagen.putpixel((x, y), matriz_2d[y][x])

    # Guardar la imagen en el mismo directorio del programa
    imagen.save(nombre_archivo)
    print(f"Imagen guardada como {nombre_archivo}")

# 🔹 Ruta de la imagen original
ruta_imagen = "eco_bebe.jpg"  # Asegúrate de que la ruta sea correcta

# Cargar la imagen como una matriz
imagen_matriz = cargar_imagen_a_matriz(ruta_imagen)

# 🔹 Agregar ruido de sal y pimienta a la imagen
porcentaje_ruido = 10  # 30% de ruido (puedes ajustar el porcentaje)
imagen_con_ruido = agregar_ruido_sal_y_pimienta(imagen_matriz, porcentaje_ruido)

# 🔹 Guardar la imagen con ruido en la misma carpeta del programa
guardar_imagen(imagen_con_ruido, "imagen_con_ruido.jpg")
