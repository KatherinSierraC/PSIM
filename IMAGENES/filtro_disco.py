import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def cargar_imagen_a_matriz(ruta_imagen):
    """Carga imagen en escala de grises y la convierte en matriz numpy."""
    imagen = Image.open(ruta_imagen).convert("L")
    return np.array(imagen, dtype=np.float64)

def filtro_disco(shape, radio):
    """Crea un filtro circular (disco) para pasar bajas en el dominio de Fourier."""
    filas, columnas = shape
    centro_x, centro_y = columnas // 2, filas // 2
    Y, X = np.ogrid[:filas, :columnas]
    distancia = np.sqrt((X - centro_x)**2 + (Y - centro_y)**2)
    return distancia <= radio  # Retorna una máscara booleana

def aplicar_filtro_fourier(imagen, radio):
    """Aplica la transformada de Fourier 2D y filtra con un disco."""
    fft = np.fft.fft2(imagen)
    fft_shift = np.fft.fftshift(fft)

    # Crear filtro
    filtro = filtro_disco(imagen.shape, radio)
    
    # Aplicar el filtro
    fft_filtrado = fft_shift * filtro
    
    # Transformada inversa
    fft_ishift = np.fft.ifftshift(fft_filtrado)
    imagen_filtrada = np.fft.ifft2(fft_ishift)
    return np.abs(imagen_filtrada)

# --------------------------
# USO

ruta = "imagen_con_ruido_gausiano.jpg"
imagen = cargar_imagen_a_matriz(ruta)

# Aplica filtro con radio 30
imagen_filtrada = aplicar_filtro_fourier(imagen, radio=30)

# Mostrar resultados
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Original con Ruido")
plt.imshow(imagen, cmap="gray")

plt.subplot(1, 2, 2)
plt.title("Filtrada (Disco)")
plt.imshow(imagen_filtrada, cmap="gray")

plt.show()
##################


import boto3
import numpy as np
import math
import io

s3 = boto3.client('s3')

def create_disk_filter(shape, radius):
    """Crea un filtro de disco en el dominio de la frecuencia"""
    rows, cols = shape
    center_row, center_col = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    distance = np.sqrt((x - center_col)**2 + (y - center_row)**2)
    disk_filter = np.zeros(shape)
    disk_filter[distance <= radius] = 1
    return disk_filter

def lambda_handler(event, context):
    # 1. Obtener imagen desde S3
    bucket = event['bucket']
    key = event['key']
    
    # Configuración para la imagen de salida
    output_bucket = bucket  # Puedes cambiarlo si quieres otro bucket
    output_key = f"filtered_{key}"  # Nombre del archivo de salida
    
    try:
        # Descargar imagen
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        
        # 2. Convertir bytes a array numpy
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        if len(image_array) >= 65536:  # 256x256
            image_array = image_array[:65536].reshape((256, 256))
        else:
            # Si la imagen es más pequeña, hacemos padding
            size = int(math.sqrt(len(image_array))) + 1
            padded = np.zeros((size, size), dtype=np.uint8)
            padded.flat[:len(image_array)] = image_array
            image_array = padded
        
        # 3. Calcular Transformada de Fourier
        fft_result = np.fft.fft2(image_array.astype(float))
        fft_shifted = np.fft.fftshift(fft_result)
        
        # 4. Aplicar filtro de disco
        disk_filter = create_disk_filter(image_array.shape, radius=30)  # Ajusta el radio según necesites
        filtered_fft = fft_shifted * disk_filter
        
        # 5. Calcular magnitud para los resultados (de la imagen filtrada)
        magnitude = np.abs(filtered_fft)
        
        # 6. Transformada inversa para obtener imagen filtrada
        inv_fft_shifted = np.fft.ifftshift(filtered_fft)
        inv_fft = np.fft.ifft2(inv_fft_shifted)
        filtered_image = np.abs(inv_fft).astype(np.uint8)
        
        # 7. Guardar imagen filtrada en S3
        # Convertir numpy array a bytes
        with io.BytesIO() as output_io:
            np.save(output_io, filtered_image)
            output_io.seek(0)
            s3.put_object(
                Bucket=output_bucket,
                Key=output_key,
                Body=output_io.read()
            )
        
        # 8. Preparar resultados
        max_freq = np.max(magnitude)
        min_freq = np.min(magnitude)
        mean_freq = np.mean(magnitude)
        
        center_value = magnitude[128, 128]  # Valor en el centro (frecuencia 0)
        edge_value = magnitude[0, 0]       # Valor en la esquina
        
        return {
            'statusCode': 200,
            'max_frequency': float(max_freq),
            'min_frequency': float(min_freq),
            'mean_frequency': float(mean_freq),
            'center_value': float(center_value),
            'edge_value': float(edge_value),
            'filtered_image_location': f"s3://{output_bucket}/{output_key}",
            'message': 'Transformada calculada, filtrada y guardada exitosamente'
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }