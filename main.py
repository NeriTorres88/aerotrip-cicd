import tkinter as tk
from pantallas import Pantallas
import sqlite3
import base  


class VentanaPrincipal(tk.Tk):
 def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("1000x750")
        self.configure(bg="#f0f8ff")

        # Contenedor principal
        self.contenedor_pantallas = tk.Frame(self, bg="white")
        self.contenedor_pantallas.pack(fill="both", expand=True)

        # Diccionario de pantallas
        self.pantallas = {}
        self.pantalla_actual = None

        # Crear pantallas
        self.crear_pantallas()

        # Crear pie de página
        self.crear_pie_pagina()

        # Mostrar pantalla inicial
        self.cambiar_pantalla("inicio")

 def crear_pantallas(self):
        """Inicializa las pantallas llamando las funciones desde pantallas.py"""
        self.pantallas["inicio"] = Pantallas.crear_pantalla_inicio(self)
        self.pantallas["nosotros"] = Pantallas.crear_pantalla_nosotros(self)
        self.pantallas["aviso_privacidad"] = Pantallas.crear_pantalla_aviso_privacidad(self)
        self.pantallas["acuerdo_confidencialidad"] = Pantallas.crear_pantalla_acuerdo_confidencialidad(self)
        self.pantallas["terminos_uso"] = Pantallas.crear_pantalla_terminos_uso(self)
        self.pantallas["login"] = Pantallas.crear_pantalla_login(self)
        self.pantallas["registro"] = Pantallas.crear_pantalla_registro(self)
        self.pantallas["recuperar_contrasena"] = Pantallas.crear_pantalla_recuperar_contrasena(self)  # Agregar pantalla
        self.pantallas["reservar_vuelo"] = None  # Inicializa esta pantalla como None
        self.pantallas["ticket_vuelo"] = None  # Inicializa la pantalla como None      
        self.pantallas["mis_reservas"] = None  # Nueva pantalla de Mis Reservas 
        self.pantallas["mis_cupones"] = Pantallas.crear_pantalla_mis_cupones(self)

 def cambiar_pantalla(self, nombre_pantalla, destino_seleccionado=None, reserva_detalles=None,mostrar_guardar=True):
    """Cambia el contenido visible de la ventana."""
    
    # Elimina el contenido de la pantalla anterior
    if self.pantalla_actual:
        self.pantalla_actual.pack_forget()

    # Verificar qué pantalla se está intentando cargar
    if nombre_pantalla == "mis_cupones":
        self.pantalla_actual = Pantallas.crear_pantalla_mis_cupones(self)

    elif nombre_pantalla == "reservar_vuelo" and destino_seleccionado:
        self.pantalla_actual = Pantallas.crear_pantalla_reservar_vuelo(self, destino_seleccionado)

    elif nombre_pantalla == "ticket_vuelo" and reserva_detalles:
        self.pantalla_actual = Pantallas.crear_pantalla_ticket_vuelo(self, reserva_detalles, mostrar_guardar)

    elif nombre_pantalla == "mis_reservas":
        self.pantalla_actual = Pantallas.crear_pantalla_mis_reservas(self)

    else:
        self.pantalla_actual = self.pantallas.get(nombre_pantalla)

    if self.pantalla_actual:
        # Actualizar el contenido de la pantalla
        self.pantalla_actual.pack(fill="both", expand=True)

 def crear_pie_pagina(self):
        """Crea el pie de página con enlaces y texto de copyright."""
        frame_footer = tk.Frame(self, bg="#f0f8ff")
        frame_footer.pack(side="bottom", fill="x", padx=20, pady=10)
   
        # Enlaces en el pie de página
        links_frame = tk.Frame(frame_footer, bg="#f0f8ff")
        links_frame.pack()

        btn_aviso_privacidad = tk.Button(
            links_frame, text="Aviso de Privacidad", command=lambda: self.cambiar_pantalla("aviso_privacidad"), bg="#f0f8ff", fg="blue", relief="flat", font=("Arial", 10), cursor="hand2"
        )
        btn_aviso_privacidad.pack(side="left", padx=10)

        # Línea divisora vertical
        separador = tk.Frame(links_frame, bg="gray", width=2, height=20)
        separador.pack(side="left", padx=10)

        btn_terminos_uso = tk.Button(
            links_frame, text="Términos de Uso", command=lambda: self.cambiar_pantalla("terminos_uso"), bg="#f0f8ff", fg="blue", relief="flat", font=("Arial", 10), cursor="hand2"
        )
        btn_terminos_uso.pack(side="left", padx=10)

        # Línea divisora vertical
        separador = tk.Frame(links_frame, bg="gray", width=2, height=20)
        separador.pack(side="left", padx=10)

        btn_confidencialidad = tk.Button(
            links_frame, text="Acuerdo de Confidencialidad", command=lambda: self.cambiar_pantalla("acuerdo_confidencialidad"), bg="#f0f8ff", fg="blue", relief="flat", font=("Arial", 10), cursor="hand2"
        )
        btn_confidencialidad.pack(side="left", padx=10)

        # Texto de copyright
        texto_footer = tk.Label(
            frame_footer,
            text="© 2025 Aerotrip - Todos los derechos reservados",
            font=("Arial", 10),
            bg="#f0f8ff",
            fg="gray",
        )
        texto_footer.pack(side="bottom", pady=5)
        
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
