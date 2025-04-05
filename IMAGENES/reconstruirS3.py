import boto3
import numpy as np
import matplotlib.pyplot as plt
import io

# Parámetros de S3
bucket_name = 'pruebapsim'  # Cambia esto por el nombre de tu bucket
object_key = 'filtered_salidas/imagen_ruido.npy'  # Cambia esto por el nombre real en tu S3

# Cliente S3
s3 = boto3.client('s3')

# Descargar archivo desde S3
response = s3.get_object(Bucket=bucket_name, Key=object_key)
npy_bytes = response['Body'].read()

# Cargar el array desde bytes (sin guardarlo en disco)
npy_array = np.load(io.BytesIO(npy_bytes))

# Visualizar la imagen en escala de grises
plt.imshow(npy_array, cmap='gray')
plt.title('Imagen descargada desde S3')
plt.axis('off')
plt.show()
