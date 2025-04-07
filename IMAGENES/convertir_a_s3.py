from matplotlib import pyplot as plt
import numpy as np
import boto3


img = plt.imread('C:\\Users\\Usuario\\Desktop\\Universidad\\PSIM\\PSIM-1\\imagen_con_ruido_alta_frecuencia.jpg')  # lee como array
if img.ndim == 3:
    img = np.mean(img, axis=2)  # convierte a escala de grises

np.save('ecografia.npy', img.astype(np.uint8))  # guarda para subir a S3




# Parámetros S3
bucket_name = 'pruebapsim'
file_path = 'ecografia.npy'              # ruta local del archivo
s3_key = 'ecografia.npy'                 # nombre que tendrá en el bucket

# Cliente S3 (asegúrate de tener tus credenciales configuradas)
s3 = boto3.client('s3')

# Subir el archivo
with open(file_path, 'rb') as file_data:
    s3.upload_fileobj(file_data, bucket_name, s3_key)

print(f"✅ Archivo subido a s3://{bucket_name}/{s3_key}")
