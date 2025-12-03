# Cesar.py

import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Funciones de cifrado y descifrado César
def cifrar_cesar(texto, desplazamiento=3):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            desplazamiento_base = 65 if caracter.isupper() else 97
            resultado += chr((ord(caracter) - desplazamiento_base + desplazamiento) % 26 + desplazamiento_base)
        else:
            resultado += caracter  # No cifrar caracteres no alfabéticos (como números y símbolos)
    return resultado

def descifrar_cesar(texto, desplazamiento=3):
    return cifrar_cesar(texto, -desplazamiento)
# Función para enviar el correo
def enviar_correo(usuario, correo_destino, contrasena_descifrada):
    servidor_smtp = "smtp.gmail.com"
    puerto = 587
    correo_origen = "utp0156963@alumno.utpuebla.edu.mx"  # Reemplázalo con tu correo
    contrasena_origen = "andromeda_yt"  # Usa la contraseña de aplicación generada

    mensaje = MIMEMultipart()
    mensaje["From"] = correo_origen
    mensaje["To"] = correo_destino
    mensaje["Subject"] = "Recuperación de contraseña"

    cuerpo_mensaje = f"""Hola {usuario},

Tu contraseña actual es: {contrasena_descifrada}

Por razones de seguridad, te recomendamos cambiarla dentro de la aplicación después de haber recibido este correo.

Saludos,
Equipo de soporte Aerotrip"""
    
    mensaje.attach(MIMEText(cuerpo_mensaje, "plain"))

    try:
        servidor = smtplib.SMTP(servidor_smtp, puerto)
        servidor.starttls()
        servidor.login(correo_origen, contrasena_origen)
        servidor.sendmail(correo_origen, correo_destino, mensaje.as_string())
        servidor.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Recuperar contraseña (solo envía la contraseña actual descifrada)
def recuperar_contrasena(correo):
    conn = sqlite3.connect("base_de_datos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT usuario, contrasena FROM usuarios WHERE correo = ?", (correo,))
    resultado = cursor.fetchone()

    if resultado:
        usuario, contrasena_encriptada = resultado
        contrasena_descifrada = descifrar_cesar(contrasena_encriptada)  # Obtiene la contraseña real

        # Enviar la contraseña actual al correo del usuario
        enviar_correo(usuario, correo, contrasena_descifrada)
    else:
        print("Correo no encontrado.")

    conn.close()

# Cambiar contraseña (cifrar y actualizar en la base de datos)
def cambiar_contrasena(usuario, nueva_contrasena):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # Cifrar la nueva contraseña
    contrasena_cifrada = cifrar_cesar(nueva_contrasena)
    
    # Actualizar la contraseña en la base de datos
    cursor.execute("UPDATE usuarios SET contrasena = ? WHERE usuario = ?", (contrasena_cifrada, usuario))
    conn.commit()
    conn.close()

    print(f"Contraseña para {usuario} actualizada correctamente")

# Verificación de inicio de sesión (comparar la contraseña ingresada)
def verificar_inicio_sesion(usuario, contrasena):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()

    if resultado:
        contrasena_cifrada_db = resultado[0]
        contrasena_descifrada = descifrar_cesar(contrasena_cifrada_db)

        if contrasena == contrasena_descifrada:
            print("Contraseña correcta")
        else:
            print("Contraseña incorrecta")
    else:
        print("Usuario no encontrado")
    
    conn.close()