import boto3
import numpy as np
import math
import io

s3 = boto3.client('s3')

def create_disk_filter(shape, radius):
    """Filtro de disco en el dominio de frecuencias."""
    rows, cols = shape
    center = (rows // 2, cols // 2)
    y, x = np.ogrid[:rows, :cols]
    distance = np.sqrt((x - center[1])**2 + (y - center[0])**2)
    return (distance <= radius).astype(np.float32)

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']
    
    # Parámetros ajustables (enfocados en ruido principal)
    disk_radius = 40  # Radio más pequeño para atacar frecuencias altas (default: 60)
    output_key = f"filtered_{key.split('.')[0]}.npy"  # Mantenemos .npy

    try:
        # 1. Descargar y preparar imagen
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        img_array = np.frombuffer(image_data, dtype=np.uint8)
        
        # Forzar tamaño 256x256 (ajustar si es necesario)
        if img_array.size >= 65536:
            img_array = img_array[:65536].reshape(256, 256)
        else:
            new_size = int(np.sqrt(img_array.size)) + 1
            img_array = np.pad(img_array, (0, new_size**2 - img_array.size)).reshape(new_size, new_size)

        # 2. Aplicar FFT + filtro de disco
        fft = np.fft.fftshift(np.fft.fft2(img_array.astype(float)))
        disk = create_disk_filter(img_array.shape, disk_radius)
        filtered_fft = fft * disk

        # 3. Reconstrucción y normalización
        reconstructed = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))
        final_image = np.clip(reconstructed, 0, 255).astype(np.uint8)

        # 4. Guardar como .npy en S3
        with io.BytesIO() as npy_buffer:
            np.save(npy_buffer, final_image)
            npy_buffer.seek(0)
            s3.put_object(
                Bucket=bucket,
                Key=output_key,
                Body=npy_buffer.read(),
                ContentType='application/octet-stream'
            )

        return {
            'statusCode': 200,
            'message': '✅ Filtro de disco aplicado (radio={}). Imagen guardada como .npy.'.format(disk_radius),
            'filtered_location': f"s3://{bucket}/{output_key}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'advice': 'Ajusta disk_radius (20-50) para controlar la eliminación de ruido.'
        }
