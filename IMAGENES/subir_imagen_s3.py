import boto3

def subir_a_s3(image_bytes, bucket_name, object_key, content_type="image/jpeg"):
    s3 = boto3.client('s3')
    
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=image_bytes,
        ContentType=content_type
        # ❌ ACL eliminado porque el bucket no lo permite
    )

    url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    return url

# Leer imagen desde archivo local
with open("imagen_con_ruido_alta_frecuencia.jpg", "rb") as f:
    imagen_bytes = f.read()

# Parámetros del bucket
bucket = 'pruebapsim'
object_key = 'salidas/imagen_ruido.png'

# Subida
url = subir_a_s3(imagen_bytes, bucket, object_key)
print("✅ Imagen subida en:", url)
