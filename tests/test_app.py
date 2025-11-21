# tests/test_app.py
import unittest
import os
import sqlite3
from pantallas import ruta_recurso, Pantallas

class TestAerotrip(unittest.TestCase):

    def test_ruta_recurso(self):
        """Verifica que la función devuelve una ruta existente."""
        ruta_logo = ruta_recurso("imagenes/Aerotrip.png")
        self.assertTrue(os.path.exists(ruta_logo), f"La ruta no existe: {ruta_logo}")

    def test_base_datos(self):
        """Verifica que la base de datos se pueda conectar."""
        try:
            conn = sqlite3.connect(ruta_recurso("base_de_datos.db"))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()
            self.assertTrue(len(tablas) > 0, "No se encontraron tablas en la base de datos")
        finally:
            conn.close()

    def test_usuario_logueado(self):
        """Verifica que la variable de usuario logueado se inicializa correctamente."""
        self.assertFalse(Pantallas.usuario_logueado)
        self.assertIsNone(Pantallas.nombre_usuario)
        self.assertIsNone(Pantallas.destino_seleccionado)
        self.assertIsNone(Pantallas.precio_seleccionado)

if __name__ == "__main__":
    unittest.main()
