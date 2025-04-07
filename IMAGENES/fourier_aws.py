import boto3
import numpy as np
import io

s3 = boto3.client('s3')

def create_disk_filter(shape, radius):
    rows, cols = shape
    center = (rows // 2, cols // 2)
    y, x = np.ogrid[:rows, :cols]
    distance = np.sqrt((x - center[1])**2 + (y - center[0])**2)
    return (distance <= radius).astype(np.float32)

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']
    
    disk_radius = 40
    output_key = f"filtered_{key.split('.')[0]}.npy"

    try:
        # Leer imagen .npy desde S3
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        img_array = np.load(io.BytesIO(image_data))

        # FFT + filtro
        fft = np.fft.fftshift(np.fft.fft2(img_array.astype(float)))
        disk = create_disk_filter(img_array.shape, disk_radius)
        filtered_fft = fft * disk

        # Reconstrucción
        reconstructed = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))
        final_image = np.clip(reconstructed, 0, 255).astype(np.uint8)

        # Guardar .npy de salida
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
            'message': f'✅ Filtro de disco aplicado (radio={disk_radius}). Imagen guardada.',
            'filtered_location': f"s3://{bucket}/{output_key}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'advice': 'Sube la imagen como archivo .npy con el array 2D.'
        }
