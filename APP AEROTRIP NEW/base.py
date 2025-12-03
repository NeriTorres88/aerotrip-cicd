import sqlite3
def conectar_base_de_datos():
    conn = sqlite3.connect('base_de_datos.db')  # Conectar a la base de datos
    cursor = conn.cursor()
    
    # Aquí puedes realizar otras operaciones en la base de datos si es necesario.
    
    conn.close()  # Cerrar la conexión cuando hayas terminado

# Llamamos a la función para conectar a la base de datos sin hacer un SELECT
conectar_base_de_datos()