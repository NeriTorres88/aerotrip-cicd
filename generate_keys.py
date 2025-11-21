from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
import base64
import os



def firmar_datos(datos_bytes, private_key_path="private.pem"):
    try:
        # Verificar si los datos no están vacíos
        if not datos_bytes:
            print("Error: Los datos a firmar están vacíos.")
            return None

        # Verificar si el archivo de clave privada existe
        if not os.path.exists(private_key_path):
            print(f"Error: El archivo de clave privada {private_key_path} no existe.")
            return None

        print(f"Cargando clave privada desde {private_key_path}")
        with open(private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        # Verificar que la clave privada se haya cargado correctamente
        if private_key is None:
            print("Error: No se pudo cargar la clave privada.")
            return None

        print(f"Clave privada cargada exitosamente.")

        # Firmar los datos
        print(f"Firmando los datos...")
        firma = private_key.sign(
            datos_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Devolver la firma como bytes
        print(f"Firma generada correctamente.")
        return firma

    except FileNotFoundError:
        print(f"Error: El archivo de clave privada {private_key_path} no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error al firmar los datos: {e}")
        return None

def verificar_firma(datos, firma_base64):
    try:
        # Verificar padding
        if len(firma_base64) % 4 != 0:
            firma_base64 += '=' * (4 - len(firma_base64) % 4)
        
        print(f"[DEBUG] Firma base64 con padding antes de decodificar: {firma_base64}")
        firma_decodificada = base64.b64decode(firma_base64)
        print(f"[DEBUG] Firma decodificada: {firma_decodificada}")
        
        # Realizar la verificación (esto dependerá del algoritmo de firma)
        # Aquí puedes agregar el código para comparar la firma con los datos
        # usando el algoritmo de firma que se haya utilizado, por ejemplo RSA o HMAC.

        # Ejemplo de verificación (esto debe ser adaptado según el tipo de firma utilizada)
        # Si es un hash, por ejemplo:
        # return firma_decodificada == hash(datos)

    except Exception as e:
        print(f"[ERROR] Error al verificar la firma: {e}")
        return False

    return True


    


    
