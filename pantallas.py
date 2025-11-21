import tkinter as tk
from tkinter import PhotoImage
from tkinter import scrolledtext,Canvas, Scrollbar,messagebox,ttk
from datetime import datetime
from PIL import Image, ImageTk 
import sqlite3
import smtplib
import re 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from tkcalendar import DateEntry
import qrcode
from email.message import EmailMessage
import hashlib
import rsa  # Asegúrate de instalarlo con `pip install rsa`
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import base64
from generate_keys import firmar_datos
from generate_keys import verificar_firma
from cesar import recuperar_contrasena,cifrar_cesar 
import os
import sys

def ruta_recurso(nombre_archivo):
    """Devuelve la ruta absoluta de un recurso (imagen o DB)"""
    import sys
    import os
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, nombre_archivo)



class Pantallas:
    
 usuario_logueado = False
 nombre_usuario = None
 destino_seleccionado = None
 precio_seleccionado = None

 

 def cambiar_pantalla(self, nombre_pantalla):
    """Cambia el contenido visible de la ventana."""
    if self.pantalla_actual:
        self.pantalla_actual.pack_forget()
    self.pantalla_actual = self.pantallas[nombre_pantalla]
    self.pantalla_actual.pack(fill="both", expand=True)
 
 def reservar(app,destino):
    """Función para manejar la reserva"""
    if not Pantallas.usuario_logueado:
        messagebox.showinfo("Iniciar sesión", "Por favor, inicie sesión para realizar la reserva.")
        app.cambiar_pantalla("login")  # Redirige a la pantalla de inicio de sesión
    else:
        # Redirige a la pantalla de reserva pasando el destino seleccionado
        app.cambiar_pantalla("reservar_vuelo", destino)  # Pasa el destino seleccionado a la pantalla de reserva



 def crear_pantalla_inicio(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")  # Azul claro

    # Contenedor principal con scrollbar
    canvas = tk.Canvas(frame, bg="#ADD8E6")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ADD8E6")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header
    header_frame = tk.Frame(scrollable_frame, bg="#f8f9fa")
    header_frame.pack(fill="x", pady=0)

    logo = PhotoImage(file=ruta_recurso("imagenes/Aerotrip.png")).subsample(6, 6)
    logo_label = tk.Label(header_frame, image=logo, bg="#f8f9fa")
    logo_label.image = logo
    logo_label.pack(side="left", padx=20)

    botones_frame = tk.Frame(header_frame, bg="#f8f9fa")
    botones_frame.pack(side="left", padx=200)

    botones = [("Inicio", "inicio"), ("Mis Reservas", "mis_reservas"), ("Nosotros", "nosotros")]
    for texto, pantalla in botones:
        btn = tk.Button(botones_frame, text=texto, command=lambda p=pantalla: app.cambiar_pantalla(p),
                        font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#007BFF",
                        relief="flat", cursor="hand2", activeforeground="#0056b3")
        btn.pack(side="left", padx=10)

    perfil_img = PhotoImage(file=ruta_recurso("imagenes/Perfil.png")).subsample(7, 7)
    btn_perfil = tk.Button(header_frame, image=perfil_img, bg="#f8f9fa",
                           command=lambda: app.cambiar_pantalla("login"), bd=0)
    btn_perfil.image = perfil_img
    btn_perfil.pack(side="right", padx=10)

    separador = tk.Frame(scrollable_frame, bg="gray", height=3, relief="sunken", bd=1)
    separador.pack(fill="x", pady=1)

    # Contenedor de destinos
    destinos_frame = tk.Frame(scrollable_frame, bg="#ADD8E6")
    destinos_frame.pack(pady=20)

    destinos = [
        {"destino": "Londres", "imagen": "london.png", "descripcion": "Londres", "precio": "$5000"},
        {"destino": "Nueva York", "imagen": "newyork.jpeg", "descripcion": "New York", "precio": "$6000"},
        {"destino": "Paris", "imagen": "paris.png", "descripcion": "Paris", "precio": "$5000"},
        {"destino": "Cancun", "imagen": "cancun.png", "descripcion": "Cancun", "precio": "$3000"},
        {"destino": "Roma", "imagen": "roma.png", "descripcion": "Roma", "precio": "$4500"},
        {"destino": "Madrid", "imagen": "madrid.png", "descripcion": "Madrid", "precio": "$5000"},
        {"destino": "Australia", "imagen": "australia.jpg", "descripcion": "Australia", "precio": "$6000"},
        {"destino": "Brasil", "imagen": "brasil.jpg", "descripcion": "Brasil", "precio": "$4000"},
        {"destino": "China", "imagen": "china.png", "descripcion": "China", "precio": "$7000"}
    ]

    imagenes_refs = []
    for i, destino in enumerate(destinos):
        fila = i // 3
        columna = i % 3

        destino_frame = tk.Frame(destinos_frame, bg="#ffffff", padx=10, pady=10, bd=2, relief="flat",
                                 highlightbackground="gray", highlightthickness=2)
        destino_frame.grid(row=fila, column=columna, padx=15, pady=15)

        img_original = Image.open(ruta_recurso(f"imagenes/{destino['imagen']}"))
        img_resized = img_original.resize((200, 150))
        imagen_destino = ImageTk.PhotoImage(img_resized)
        imagenes_refs.append(imagen_destino)

        img_label = tk.Label(destino_frame, image=imagen_destino, bg="#ffffff")
        img_label.image = imagen_destino
        img_label.pack()

        descripcion_label = tk.Label(destino_frame, text=destino["descripcion"],
                                     font=("Arial", 12, "bold"), bg="#ffffff", wraplength=200)
        descripcion_label.pack(pady=5)

        viaje_label = tk.Label(destino_frame, text="Viaje de ida y vuelta", font=("Arial", 10), bg="#ffffff")
        viaje_label.pack(pady=5)

        # Actualización del precio con la nueva nota
        precio_label = tk.Label(destino_frame, text=f"Precio desde {destino['precio']} (varía según pasajeros y clase)", 
                                font=("Arial", 10), bg="#ffffff", wraplength=200, justify="center")
        precio_label.pack(pady=5)

        reservar_btn = tk.Button(destino_frame, text="Reservar", font=("Arial", 10), bg="blue", fg="white",
                     relief="flat", cursor="hand2",
                     command=lambda d=destino: Pantallas.reservar(app, d))
        reservar_btn.pack(pady=10)

    frame.imagenes_refs = imagenes_refs

    return frame
 


 def crear_pantalla_reservar_vuelo(app, destino_seleccionado):
    """Crea la pantalla de reservar vuelo con el destino seleccionado"""
    
    if destino_seleccionado is None:
        messagebox.showerror("Error", "No se ha seleccionado un destino.")
        return app.cambiar_pantalla("inicio")

    # Variables locales para la función
    precio_base = float(destino_seleccionado.get("precio", "2000").replace("$", "").replace(",", ""))
    precio_final = precio_base  # Mantén un precio final para aplicar descuento
    descuento_aplicado = 0
    estado = {"cupón_validado": False, "descuento_aplicado": 0}

    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")
    
    tk.Label(frame, text="Reserva tu Vuelo", font=("Arial", 18, "bold"), bg="#ADD8E6").pack(pady=20)
    
    container = tk.Frame(frame, bg="white", bd=4, relief="groove", padx=20, pady=20)
    container.pack(pady=20, padx=50)

    tk.Label(container, text="Destino:", font=("Arial", 12, "bold"), bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=5, padx=5)
    tk.Label(container, text=destino_seleccionado['destino'], font=("Arial", 12, "bold"), bg="white").grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(container, text="Precio:", font=("Arial", 12, "bold"), bg="white", anchor="w").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    precio_label = tk.Label(container, text=f"${precio_base:.2f}", font=("Arial", 12, "bold"), bg="white")
    precio_label.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(container, text="Cupón de descuento:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=5, padx=5)
    cupon_entry = tk.Entry(container, font=("Arial", 12), bd=1, relief="solid", width=30, bg="white", fg="black")
    cupon_entry.grid(row=2, column=1, pady=5)

    # Obtener el nombre del usuario logueado
    nombre_usuario = Pantallas.nombre_usuario if Pantallas.usuario_logueado else ""

    tk.Label(container, text="Nombre Completo:", font=("Arial", 12), bg="white", anchor="w").grid(row=3, column=0, sticky="w", pady=5, padx=5)
    nombre_entry = tk.Entry(container, font=("Arial", 12), bd=1, relief="solid", width=30, bg="white", fg="black")
    nombre_entry.grid(row=3, column=1, pady=5)
    nombre_entry.insert(0, nombre_usuario)

    if Pantallas.usuario_logueado:
        nombre_entry.config(state="disabled")

    # Etiqueta y campo para la fecha de ida
    tk.Label(container, text="Fecha de Ida:", font=("Arial", 12), bg="white", anchor="w").grid(row=4, column=0, sticky="w", pady=5, padx=5)
    fecha_ida_entry = DateEntry(container, font=("Arial", 12), width=27, background='white', foreground='black', borderwidth=2)
    fecha_ida_entry.grid(row=4, column=1, pady=5)

    # Etiqueta y campo para la fecha de regreso
    tk.Label(container, text="Fecha de Regreso:", font=("Arial", 12), bg="white", anchor="w").grid(row=5, column=0, sticky="w", pady=5, padx=5)
    fecha_regreso_entry = DateEntry(container, font=("Arial", 12), width=27, background='white', foreground='black', borderwidth=2)
    fecha_regreso_entry.grid(row=5, column=1, pady=5)

    # Dejar la fecha de regreso igual a la de ida por defecto
    fecha_regreso_entry.set_date(fecha_ida_entry.get_date())

    # Número de Pasajeros
    tk.Label(container, text="Número de Pasajeros:", font=("Arial", 12), bg="white", anchor="w").grid(row=6, column=0, sticky="w", pady=5, padx=5)
    pasajeros_combo = ttk.Combobox(container, font=("Arial", 12), values=["1", "2", "3", "4", "5"], width=28)
    pasajeros_combo.grid(row=6, column=1, pady=5)
    pasajeros_combo.current(0)

    # Clase de vuelo
    tk.Label(container, text="Clase:", font=("Arial", 12), bg="white", anchor="w").grid(row=7, column=0, sticky="w", pady=5, padx=5)
    clase_combo = ttk.Combobox(container, font=("Arial", 12), values=["Economica", "Business", "Primera"], width=28)
    clase_combo.grid(row=7, column=1, pady=5)
    clase_combo.current(0)

    # Datos de pago
    tk.Label(container, text="Número de tarjeta:", font=("Arial", 12), bg="white", anchor="w").grid(row=8, column=0, sticky="w", pady=5, padx=5)
    tarjeta_entry = tk.Entry(container, font=("Arial", 12), bd=1, relief="solid", width=30, bg="white", fg="gray")
    tarjeta_entry.grid(row=8, column=1, pady=5)
    tarjeta_entry.insert(0, "Ejemplo: 1234 5678 9876 5432")

    tk.Label(container, text="Fecha de vencimiento (MM/AA):", font=("Arial", 12), bg="white", anchor="w").grid(row=9, column=0, sticky="w", pady=5, padx=5)
    vencimiento_entry = tk.Entry(container, font=("Arial", 12), bd=1, relief="solid", width=15, bg="white", fg="gray")
    vencimiento_entry.grid(row=9, column=1, pady=5)
    vencimiento_entry.insert(0, "Ejemplo: 12/25")

    tk.Label(container, text="CVV:", font=("Arial", 12), bg="white", anchor="w").grid(row=10, column=0, sticky="w", pady=5, padx=5)
    cvv_entry = tk.Entry(container, font=("Arial", 12), bd=1, relief="solid", width=10, bg="white", fg="gray")
    cvv_entry.grid(row=10, column=1, pady=5)
    cvv_entry.insert(0, "Ejemplo: 123")  # Agregar el ejemplo en claro

    # Función para limpiar los ejemplos
    def limpiar_ejemplo(entry, ejemplo):
        if entry.get() == ejemplo:
            entry.delete(0, tk.END)

    def restaurar_ejemplo(entry, ejemplo):
        if entry.get() == "":
            entry.insert(0, ejemplo)

    # Asociar la limpieza y restauración de ejemplos con los eventos correspondientes
    tarjeta_entry.bind("<FocusIn>", lambda event: limpiar_ejemplo(tarjeta_entry, "Ejemplo: 1234 5678 9876 5432"))
    tarjeta_entry.bind("<FocusOut>", lambda event: restaurar_ejemplo(tarjeta_entry, "Ejemplo: 1234 5678 9876 5432"))

    vencimiento_entry.bind("<FocusIn>", lambda event: limpiar_ejemplo(vencimiento_entry, "Ejemplo: 12/25"))
    vencimiento_entry.bind("<FocusOut>", lambda event: restaurar_ejemplo(vencimiento_entry, "Ejemplo: 12/25"))

    cvv_entry.bind("<FocusIn>", lambda event: limpiar_ejemplo(cvv_entry, "Ejemplo: 123"))
    cvv_entry.bind("<FocusOut>", lambda event: restaurar_ejemplo(cvv_entry, "Ejemplo: 123"))

    def actualizar_precio(*args):
        """Actualiza el precio según número de pasajeros, clase y duración del viaje"""
        pasajeros = int(pasajeros_combo.get())
        clase = clase_combo.get()

        # Calculamos el precio según la clase seleccionada
        precio_final = precio_base  # Volver a establecer el precio base

        if clase == "Business":
            precio_final *= 1.5
        elif clase == "Primera":
            precio_final *= 2

        # Aplicar el descuento si se ha validado un cupón
        if estado["cupón_validado"]:
            precio_final -= (precio_base * estado["descuento_aplicado"] / 100)

        # Multiplicar por el número de pasajeros
        precio_final *= pasajeros

        # Verificar si la duración del viaje excede una semana
        fecha_ida = fecha_ida_entry.get_date()
        fecha_regreso = fecha_regreso_entry.get_date()
        diferencia_dias = (fecha_regreso - fecha_ida).days

        if diferencia_dias > 7:
            precio_final *= 1.2
            messagebox.showinfo("Advertencia", "Su estancia excede una semana, se aplicará un costo adicional del 20%.")

        # Actualizar el precio en la etiqueta
        precio_label.config(text=f"${precio_final:.2f}")
        return precio_final  # Devolvemos el valor actualizado

    pasajeros_combo.bind("<<ComboboxSelected>>", actualizar_precio)
    clase_combo.bind("<<ComboboxSelected>>", actualizar_precio)
    fecha_ida_entry.bind("<<DateEntrySelected>>", actualizar_precio)
    fecha_regreso_entry.bind("<<DateEntrySelected>>", actualizar_precio)

    def validar_cupon():
        cupon_codigo = cupon_entry.get().strip()

        if not cupon_codigo:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un código de cupón.")
            return

        if cupon_codigo and not estado["cupón_validado"]:
            conn = sqlite3.connect("base_de_datos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT descuento, usado FROM cupones WHERE codigo = ?", (cupon_codigo,))
            cupon = cursor.fetchone()

            if cupon:
                descuento, usado = cupon

                if usado == 0:  # Si no ha sido usado
                    # Aplicar el descuento en el precio final sin modificar el número de pasajeros o clase
                    estado["descuento_aplicado"] = descuento
                    estado["cupón_validado"] = True

                    # Actualizamos el precio final aplicando el descuento
                    actualizar_precio()

                    messagebox.showinfo("Éxito", f"Cupón aplicado. ¡Descuento de {descuento}%!")
                    cupon_entry.config(state="disabled")
                else:
                    messagebox.showerror("Error", "Este cupón ya ha sido utilizado.")
            else:
                messagebox.showerror("Error", "El código de cupón no es válido.")

            conn.close()
        elif estado["cupón_validado"]:
            messagebox.showwarning("Advertencia", "Ya has aplicado un cupón.")

    def validar_tarjeta():
        tarjeta = tarjeta_entry.get().strip().replace(" ", "")
        if not tarjeta.isdigit() or len(tarjeta) != 16:
            messagebox.showerror("Error", "El número de tarjeta debe contener exactamente 16 dígitos.")
            return False
        return True

    def validar_vencimiento():
        vencimiento = vencimiento_entry.get().strip()
        try:
            mes, anio = map(int, vencimiento.split("/"))
            if mes < 1 or mes > 12:
                messagebox.showerror("Error", "El mes de vencimiento debe estar entre 01 y 12.")
                return False
            if anio < 22:
                messagebox.showerror("Error", "El año de vencimiento no es válido.")
                return False
        except ValueError:
            messagebox.showerror("Error", "El formato de fecha de vencimiento es incorrecto. Use MM/AA.")
            return False
        return True

    def validar_cvv():
        cvv = cvv_entry.get().strip()
        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showerror("Error", "El CVV debe contener exactamente 3 dígitos.")
            return False
        return True
    

    def confirmar_reserva():
        # Mover la validación de pago aquí dentro
        if not validar_tarjeta() or not validar_vencimiento() or not validar_cvv():
            return

        # Solo proceder si el usuario confirma
        confirmacion = messagebox.askyesno(
            "Confirmación", 
            f"¿Está seguro de hacer el pago por {precio_label.cget('text')}?"
        )
        
        if not confirmacion:
            return  # Si el usuario dice "No", salir de la función

        # Procesar reserva solo después de la confirmación
        tarjeta_ultimos_3 = "*" * 13 + tarjeta_entry.get().strip().replace(" ", "")[-3:]
        vencimiento_anio = "*" * 2 + vencimiento_entry.get().strip().split("/")[1]

        reserva_detalles = {
        'destino': str(destino_seleccionado['destino']),
        'precio': float(precio_label.cget("text").replace('$', '').replace(',', '')),
        'nombre_usuario': str(Pantallas.nombre_usuario),
        'fecha_ida': str(fecha_ida_entry.get_date()),  # Convertir a string
        'fecha_regreso': str(fecha_regreso_entry.get_date()),
        'pasajeros': str(pasajeros_combo.get()),
        'clase': str(clase_combo.get()),
        'tarjeta_ultimos_3': str(tarjeta_ultimos_3),
        'vencimiento_anio': str(vencimiento_anio)
         }
        
        print(f"Datos a firmar: {reserva_detalles}")
        # Antes de firmar


        datos_para_firma = {key: value for key, value in reserva_detalles.items() if key != 'firma'}
        datos_serializados = json.dumps(datos_para_firma, sort_keys=True, ensure_ascii=False).encode('utf-8')
    
        firma_bytes = firmar_datos(datos_serializados)

        if not firma_bytes:
         messagebox.showerror("Error", "No se pudo generar la firma.")
         return

        firma_base64 = base64.b64encode(firma_bytes).decode('utf-8')
        reserva_detalles['firma'] = firma_base64
        

        if estado["cupón_validado"]:
            conn = sqlite3.connect("base_de_datos.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE cupones SET usado = 1 WHERE codigo = ?", (cupon_entry.get().strip(),))
            conn.commit()
            conn.close()

        # Cambiar a pantalla de ticket
        app.cambiar_pantalla("ticket_vuelo", reserva_detalles=reserva_detalles)

    btn_validar_cupon = tk.Button(container, text="Validar Cupón", font=("Arial", 12, "bold"), bg="#28A745", fg="white", relief="flat", width=12, cursor="hand2", command=validar_cupon)
    btn_validar_cupon.grid(row=2, column=2, padx=5, pady=10)

    btn_confirmar = tk.Button(container, text="Confirmar Reserva", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", relief="flat", width=20, cursor="hand2", command=confirmar_reserva)
    btn_confirmar.grid(row=12, column=0, columnspan=2, pady=20)

    btn_volver = tk.Button(container, text="Cancelar", font=("Arial", 12, "bold"), bg="#FF0000", fg="white", relief="flat", width=20, cursor="hand2", command=lambda: app.cambiar_pantalla("inicio"))
    btn_volver.grid(row=13, column=0, columnspan=2, pady=10)

    return frame
 
 def crear_pantalla_ticket_vuelo(app, reserva_detalles,mostrar_guardar=True):
    """Crea la pantalla del ticket con los detalles de la reserva."""
    print(f"[DEBUG] Datos recibidos en ticket_vuelo: {reserva_detalles}")
    
    try:
        # Verificación de firma (silenciosa, solo para logging)
        if 'firma' in reserva_detalles:
            firma_base64 = reserva_detalles['firma']
            try:
                # Limpiar la firma base64 (eliminar saltos de línea y espacios)
                firma_base64 = firma_base64.strip()
                print(f"Firma base64 (limpia): {firma_base64}")
                
                # Intentar decodificar la firma base64
                firma_decodificada = base64.b64decode(firma_base64)
                
                # Verificar la firma
                datos_sin_firma = {key: value for key, value in reserva_detalles.items() if key != 'firma'}
                datos_serializados = json.dumps(datos_sin_firma, sort_keys=True, ensure_ascii=False).encode('utf-8')
                
                if verificar_firma(datos_serializados, firma_base64):
                    reserva_detalles['verificado'] = True
                    print("[DEBUG] Firma verificada exitosamente.")
                    # Mostrar un mensaje indicando que el ticket no ha sido alterado
                    messagebox.showinfo("Verificación Exitosa", "El ticket no ha sido alterado.")
                else:
                    reserva_detalles['verificado'] = False
                    print("[DEBUG] La firma no es válida.")
                    # Si la firma no es válida, evitar mostrar la información
                    messagebox.showerror("Error", "Los datos del ticket han sido alterados. No se puede mostrar.")
                    return  # Salir de la función sin mostrar la pantalla del ticket
            except Exception as e:
                print(f"[DEBUG] Error en verificación de firma: {e}")
                reserva_detalles['verificado'] = None
                print("[DEBUG] No se pudo verificar la firma.")
    except Exception as e:
        print(f"[ERROR] Error en la creación de la pantalla del ticket: {e}")

    # Mostrar el ticket
    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")
    tk.Label(frame, text="Detalles de la Reserva", font=("Arial", 18, "bold"), bg="#ADD8E6").pack(pady=20)

    container = tk.Frame(frame, bg="white", bd=4, relief="groove", padx=20, pady=20)
    container.pack(pady=20, padx=130, fill="both", expand=True)

    detalles_frame = tk.Frame(container, bg="white")
    detalles_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Formatear precio correctamente
    try:
        if isinstance(reserva_detalles['precio'], str):
            precio_num = float(reserva_detalles['precio'].replace('$', '').replace(',', ''))
        else:
            precio_num = float(reserva_detalles['precio'])
        precio_formateado = f"${precio_num:,.2f}"
    except (ValueError, TypeError):
        precio_formateado = "Precio no disponible"

    detalles = [
        ("Destino:", reserva_detalles['destino']),
        ("Precio:", precio_formateado),
        ("Nombre Completo:", reserva_detalles['nombre_usuario']),
        ("Fecha de Ida:", reserva_detalles['fecha_ida']),
        ("Fecha de Regreso:", reserva_detalles['fecha_regreso']),
        ("Número de Pasajeros:", reserva_detalles['pasajeros']),
        ("Clase:", reserva_detalles['clase']),
        ("Número de tarjeta:", reserva_detalles['tarjeta_ultimos_3']),
        ("Vencimiento:", reserva_detalles['vencimiento_anio'])
    ]
    

    for i, (label, value) in enumerate(detalles):
        tk.Label(detalles_frame, text=label, font=("Arial", 12, "bold"), bg="white", fg="black", anchor="w").grid(row=i, column=0, sticky="w", pady=5, padx=5)
        tk.Label(detalles_frame, text=value, font=("Arial", 12), bg="white", fg="black").grid(row=i, column=1, sticky="w", pady=5)

    # Generar el QR con datos seguros
    qr_frame = tk.Frame(container, bg="white")
    qr_frame.grid(row=0, column=1, padx=20, pady=5, sticky="e")

    qr_data = {
        'destino': reserva_detalles['destino'],
        'precio': precio_formateado,
        'nombre': reserva_detalles['nombre_usuario'],
        'fechas': f"{reserva_detalles['fecha_ida']} a {reserva_detalles['fecha_regreso']}",
        'id_unico': f"{hash(frozenset(reserva_detalles.items())):x}"[:8]
    }

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img_resized = img.resize((200, 200))
    img_path = "reserva_qr_temp.png"
    img_resized.save(img_path)

    qr_image = ImageTk.PhotoImage(img_resized)
    qr_label = tk.Label(qr_frame, image=qr_image, bg="white")
    qr_label.image = qr_image
    qr_label.pack(pady=10)

    # Contenedor de botones
    button_frame = tk.Frame(container, bg="white")
    button_frame.grid(row=1, column=0, columnspan=2, pady=20)

    def insertar_reserva():
        # Insertar en la base de datos solo cuando se haga clic en "Guardar"
        try:
            conn = sqlite3.connect("base_de_datos.db")
            cursor = conn.cursor()

            cursor.execute(""" 
                SELECT COUNT(*) FROM reservas 
                WHERE nombre_usuario = ? AND destino = ? AND fecha_ida = ? 
            """, (
                reserva_detalles.get('nombre_usuario', ''),
                reserva_detalles.get('destino', ''),
                reserva_detalles.get('fecha_ida', '')
            ))

            if cursor.fetchone()[0] == 0:  # Solo insertar si no existe
                cursor.execute(""" 
                    INSERT INTO reservas 
                    (destino, precio, nombre_usuario, fecha_ida, fecha_regreso, 
                    pasajeros, clase, tarjeta_ultimos_3, vencimiento_anio, firma)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    reserva_detalles.get('destino', ''),
                    float(reserva_detalles.get('precio', 0)),
                    reserva_detalles.get('nombre_usuario', ''),
                    reserva_detalles.get('fecha_ida', ''),
                    reserva_detalles.get('fecha_regreso', ''),
                    int(reserva_detalles.get('pasajeros', 1)),
                    reserva_detalles.get('clase', ''),
                    reserva_detalles.get('tarjeta_ultimos_3', ''),
                    reserva_detalles.get('vencimiento_anio', ''),
                    reserva_detalles.get('firma')
                ))
                conn.commit()
                messagebox.showinfo("Éxito", "Reserva guardada en la base de datos")
            else:
                messagebox.showinfo("Información", "Ya existe una reserva con los mismos datos.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar la reserva: {e}")
        finally:
            conn.close()

    def confirmar_guardar_y_salir():
        """Función para confirmar si quiere guardar antes de salir."""
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de guardar los cambios y salir?")
        if respuesta:  # Si el usuario confirma
            insertar_reserva()  # Guardar la reserva
            app.cambiar_pantalla("inicio")  # Cambiar a la pantalla de inicio




    def enviar_por_correo():
            from_email = "utp0156963@alumno.utpuebla.edu.mx"
            to_email = Pantallas.correo_usuario

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = "Detalles de su reserva de vuelo"

            body = f"""
            Estimado/a {reserva_detalles['nombre_usuario']},

            Gracias por realizar su reserva con nosotros. Aquí están los detalles de su vuelo:

            Destino: {reserva_detalles['destino']}
            Precio: {precio_formateado}
            Nombre Completo: {reserva_detalles['nombre_usuario']}
            Fecha de Ida: {reserva_detalles['fecha_ida']}
            Fecha de Regreso: {reserva_detalles['fecha_regreso']}
            Número de Pasajeros: {reserva_detalles['pasajeros']}
            Clase: {reserva_detalles['clase']}
            Tarjeta: {reserva_detalles['tarjeta_ultimos_3']}
            Vencimiento: {reserva_detalles['vencimiento_anio']}

            Adjuntamos el código QR con la información de su reserva.

            Atentamente,
            Aerotrip
            """
            msg.attach(MIMEText(body, 'plain'))

            try:
                with open(img_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename="reserva_qr.png")
                    msg.attach(img)
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(from_email, "andromeda_yt")
                server.sendmail(from_email, to_email, msg.as_string())
                server.quit()
                messagebox.showinfo("Éxito", "Detalles enviados por correo.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")
            finally:
                import os
                if os.path.exists(img_path):
                    os.remove(img_path)

    # Botón de "Enviar por Correo"
    btn_enviar_correo = tk.Button(button_frame, text="Enviar por Correo", font=("Arial", 12, "bold"),
                                  bg="#007BFF", fg="white", relief="flat", width=20, cursor="hand2",
                                  command=enviar_por_correo)
    btn_enviar_correo.pack(side="left", padx=10)

    if mostrar_guardar:
        btn_guardar = tk.Button(button_frame, text="Guardar y Salir", font=("Arial", 12, "bold"),
                                bg="green", fg="white", relief="flat", width=20, cursor="hand2",
                                command=confirmar_guardar_y_salir)
        btn_guardar.pack(side="left", padx=10)
    else:
        btn_regresar = tk.Button(button_frame, text="Regresar a Mis Reservas", font=("Arial", 12, "bold"),
                                 bg="lightblue", fg="black", relief="flat", width=20, cursor="hand2",
                                 command=lambda: app.cambiar_pantalla("mis_reservas"))
        btn_regresar.pack(side="left", padx=10)

    return frame


    

 
 def crear_pantalla_login(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="lightblue")

    btn_regresar = tk.Button(frame, text="←", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="lightblue", fg="blue", relief="flat", font=("Arial", 20), cursor="hand2")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    container = tk.Frame(frame, bg="white", bd=4, relief="groove")
    container.pack(pady=100, padx=50, ipadx=20, ipady=20)

    tk.Label(container, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

    tk.Label(container, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=5)
    usuario_entry = tk.Entry(container, font=("Arial", 12), bd=2, relief="solid", width=25)
    usuario_entry.pack(pady=5)

    tk.Label(container, text="Contraseña:", font=("Arial", 12), bg="white").pack(pady=5)
    contrasena_entry = tk.Entry(container, font=("Arial", 12), show="*", bd=2, relief="solid", width=25)
    contrasena_entry.pack(pady=5)

    def validar_datos():
        usuario = usuario_entry.get().strip()
        contrasena = contrasena_entry.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña.")
            return

        contrasena_cifrada = cifrar_cesar(contrasena, 3)  # Cifra la contraseña antes de compararla

        conn = sqlite3.connect("base_de_datos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, correo FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena_cifrada))
        usuario_encontrado = cursor.fetchone()
        conn.close()

        if usuario_encontrado:
            Pantallas.nombre_usuario = usuario_encontrado[0]
            Pantallas.correo_usuario = usuario_encontrado[1]
            Pantallas.usuario_logueado = True
            messagebox.showinfo("Éxito", f"¡Bienvenido, {Pantallas.nombre_usuario}!")
            app.cambiar_pantalla("inicio")

            # Mostrar el botón de cupones si el usuario está logueado
            btn_mis_cupones = tk.Button(container, text="Mis Cupones", font=("Arial", 12, "bold"), bg="purple", fg="white",
                                        relief="flat", width=20, cursor="hand2", command=lambda: app.cambiar_pantalla("mis_cupones"))
            btn_mis_cupones.pack(pady=10)  # Asegurarse de que el botón se empuje hacia abajo

            # Mostrar el botón de "Cerrar Sesión"
            btn_cerrar_sesion.pack(pady=10)

            # Esconder otros widgets como el botón de "Ingresar", etc.
            for widget in container.winfo_children():
                if widget != btn_mis_cupones and widget != btn_cerrar_sesion:
                    widget.pack_forget()

        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    btn_ingresar = tk.Button(container, text="Ingresar", font=("Arial", 12, "bold"), bg="#007BFF", fg="white",
                             relief="flat", width=20, cursor="hand2", command=validar_datos)
    btn_ingresar.pack(pady=10)

    btn_registro = tk.Button(container, text="Crear Cuenta", font=("Arial", 12, "bold"), bg="green", fg="white",
                             relief="flat", width=20, cursor="hand2", command=lambda: app.cambiar_pantalla("registro"))
    btn_registro.pack(pady=5)

    btn_recuperar_contrasena = tk.Button(container, text="¿Olvidaste tu contraseña?", font=("Arial", 10), fg="blue", bg="white",
                                         relief="flat", cursor="hand2", command=lambda: app.cambiar_pantalla("recuperar_contrasena"))
    btn_recuperar_contrasena.pack(pady=5)


    def cerrar_sesion():
        if not Pantallas.usuario_logueado:
            messagebox.showerror("Error", "No hay una sesión activa.")
            return

        def confirmar_cerrar_sesion():
            respuesta = messagebox.askyesno("Confirmar", f"{Pantallas.nombre_usuario}, ¿quieres cerrar sesión?")
            if respuesta:
                messagebox.showinfo("Cerrar sesión", f"Hasta luego, {Pantallas.nombre_usuario}.")

                Pantallas.usuario_logueado = False
                Pantallas.nombre_usuario = None
                Pantallas.correo_usuario = None

                app.cambiar_pantalla("login")

                usuario_entry.delete(0, tk.END)
                contrasena_entry.delete(0, tk.END)

                btn_cerrar_sesion.pack_forget()

                # Restablecer los widgets iniciales
                for widget in container.winfo_children():
                    widget.pack_forget()

                btn_regresar.pack(anchor="w", padx=20, pady=10)
                container.pack(pady=100, padx=50, ipadx=20, ipady=20)

                tk.Label(container, text="Iniciar Sesión", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
                tk.Label(container, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=5)
                usuario_entry.pack(pady=5)
                tk.Label(container, text="Contraseña:", font=("Arial", 12), bg="white").pack(pady=5)
                contrasena_entry.pack(pady=5)
                btn_ingresar.pack(pady=10)
                btn_registro.pack(pady=5)
                btn_recuperar_contrasena.pack(pady=5)

        confirmar_cerrar_sesion()

    btn_cerrar_sesion = tk.Button(container, text="Cerrar sesión", font=("Arial", 12, "bold"), bg="red", fg="white",
                                  relief="flat", width=20, cursor="hand2", command=cerrar_sesion)
    btn_cerrar_sesion.pack_forget()  # Se esconde al principio

    return frame
 

 def crear_pantalla_mis_cupones(app):
    if not Pantallas.usuario_logueado:
        app.cambiar_pantalla("login")
        return

    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")
    frame.pack(fill="both", expand=True)  # Asegúrate de que el frame se agregue al contenedor

    # Título
    tk.Label(frame, text="Mis Cupones", font=("Arial", 18, "bold"), bg="#ADD8E6").pack(pady=20)

    # Botón de Regresar
    btn_regresar = tk.Button(frame, text="← Regresar", font=("Arial", 12, "bold"), bg="lightblue", fg="blue",
                             relief="flat", cursor="hand2", command=lambda: app.cambiar_pantalla("login"))
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Contenedor de los cupones
    container = tk.Frame(frame, bg="white", bd=4, relief="groove", padx=20, pady=20)
    container.pack(pady=20, padx=50, fill="both", expand=True)

    # Obtener los cupones del usuario logueado
    conn = sqlite3.connect("base_de_datos.db")
    cursor = conn.cursor()

    # Buscar el id_usuario utilizando el nombre del usuario
    cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (Pantallas.nombre_usuario,))
    usuario_id = cursor.fetchone()

    if usuario_id:
        # Ahora obtienes los cupones del usuario utilizando el id_usuario
        cursor.execute("SELECT id, codigo, descuento, usado FROM cupones WHERE id_usuario = ?", (usuario_id[0],))
        cupones = cursor.fetchall()
        conn.close()

        if cupones:
            # Mostrar cupones
            for i, cupon in enumerate(cupones):
                label_text = f"Código: {cupon[1]} | Descuento: {cupon[2]}%"
                if cupon[3] == 1:
                    label_text += " (Usado)"
                
                tk.Label(container, text=label_text, font=("Arial", 12), bg="white").grid(row=i, column=0, sticky="w", pady=5, padx=5)

                # Botón para copiar el código del cupón si no ha sido usado
                if cupon[3] == 0:
                    btn_copiar = tk.Button(container, text="Copiar Código", font=("Arial", 10), bg="#28A745", fg="white", relief="flat", cursor="hand2", command=lambda c=cupon[1]: copiar_codigo(c))
                    btn_copiar.grid(row=i, column=1, pady=5)
        else:
            tk.Label(container, text="No tienes cupones disponibles.", font=("Arial", 12), bg="white").pack(pady=20)
    else:
        messagebox.showerror("Error", "No se ha encontrado el usuario con ese nombre.")

    def copiar_codigo(cupon_codigo):
        # Copiar el código al portapapeles utilizando tkinter
        app.clipboard_clear()  # Limpiar el portapapeles
        app.clipboard_append(cupon_codigo)  # Añadir el código al portapapeles
        app.update()  # Actualizar el portapapeles
        messagebox.showinfo("Éxito", f"El código '{cupon_codigo}' ha sido copiado al portapapeles.")

    return frame



 
 def crear_pantalla_mis_reservas(app):
    """Crea la pantalla para mostrar las reservas del usuario logueado."""
    frame = tk.Frame(app.contenedor_pantallas, bg="lightblue")

    tk.Label(frame, text="Mis Reservas", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=20)

    container = tk.Frame(frame, bg="white", bd=4, relief="groove", padx=20, pady=20)
    container.pack(pady=20, padx=50, fill="both", expand=True)

    def cargar_reservas():
        """Carga las reservas del usuario logueado desde la base de datos."""
        for widget in container.winfo_children():
            widget.destroy()

        if not Pantallas.usuario_logueado:
            tk.Label(container, 
                    text="Debe iniciar sesión para ver sus reservas.", 
                    font=("Arial", 12), 
                    bg="white").pack(pady=10)
            return

        conn = sqlite3.connect("base_de_datos.db")
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT 
                id, destino, precio, nombre_usuario, 
                strftime('%Y-%m-%d', fecha_ida) as fecha_ida,
                strftime('%Y-%m-%d', fecha_regreso) as fecha_regreso,
                pasajeros, clase, tarjeta_ultimos_3, 
                vencimiento_anio, firma 
            FROM reservas 
            WHERE nombre_usuario = ? 
            ORDER BY fecha_ida DESC
        """, (Pantallas.nombre_usuario,))
        reservas = cursor.fetchall()
        conn.close()

        if not reservas:
            tk.Label(container, 
                    text="No tienes reservas registradas.", 
                    font=("Arial", 12), 
                    bg="white").pack(pady=10)
            return

        canvas = tk.Canvas(container, bg="white")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for reserva in reservas:
            frame_reserva = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
            frame_reserva.pack(pady=5, padx=5, fill="x")

            # Formatear precio correctamente
            try:
                precio = float(reserva[2])
                precio_formateado = f"${precio:,.2f}"
            except (ValueError, TypeError):
                precio_formateado = "Precio no disponible"

            tk.Label(
                frame_reserva,
                text=f"{reserva[1]} - {precio_formateado} - Ida: {reserva[4]}",
                font=("Arial", 12),
                bg="white"
            ).pack(side="left", padx=10)

            btn_ver = tk.Button(
                frame_reserva,
                text="Ver Detalles",
                font=("Arial", 10, "bold"),
                bg="#4CAF50",
                fg="white",
                relief="flat",
                width=10,
                cursor="hand2",
                command=lambda r=reserva: mostrar_ticket(r)
            )
            btn_ver.pack(side="right", padx=5)

    def mostrar_ticket(reserva):
     """Muestra el ticket con verificación de integridad de datos"""
     try:
        # 1. Extraer y convertir datos de forma segura
        try:
            precio = float(reserva[2]) if reserva[2] is not None else 0.0
            precio_formateado = f"${precio:,.2f}"
        except (ValueError, TypeError) as e:
            print(f"Error al convertir precio: {e}")
            precio_formateado = "Precio no disponible"

        # 2. Preparar estructura para verificación
        datos_verificacion = {
            'destino': str(reserva[1]) if reserva[1] else "",
            'precio': precio,  # Usar el valor float para verificación
            'nombre_usuario': str(reserva[3]) if reserva[3] else "",
            'fecha_ida': str(reserva[4]) if reserva[4] else "",
            'fecha_regreso': str(reserva[5]) if reserva[5] else "",
            'pasajeros': str(reserva[6]) if reserva[6] else "",
            'clase': str(reserva[7]) if reserva[7] else "",
            'tarjeta_ultimos_3': str(reserva[8]) if reserva[8] else "",
            'vencimiento_anio': str(reserva[9]) if reserva[9] else ""
        }

        # 3. Verificación de firma (si existe)
        firma_valida = None
        if len(reserva) > 10 and reserva[10]:  # Si hay firma almacenada
            try:
                from generate_keys import verificar_firma
                import json
                import base64
                
                # Verificar si la firma está en base64
                try:
                    firma_base64 = reserva[10].strip()
                    firma_decodificada = base64.b64decode(firma_base64)
                    firma_valida = verificar_firma(datos_verificacion, firma_base64)
                except Exception as e:
                    print(f"Error al decodificar base64: {e}")
                    firma_valida = False
                    
                    # Si no es base64, intentar con hexadecimal
                    try:
                        firma_valida = verificar_firma(datos_verificacion, bytes.fromhex(reserva[10]))
                    except Exception as hex_e:
                        print(f"Error al decodificar hexadecimal: {hex_e}")
                        firma_valida = False

                if not firma_valida:
                    messagebox.showwarning(
                        "Advertencia de Seguridad", 
                        "¡Atención! Los datos podrían haber sido alterados."
                    )
                else:
                    # Mostrar mensaje de ticket no alterado
                    messagebox.showinfo(
                        "Ticket Verificado",
                        "El ticket no ha sido alterado."
                    )
            except Exception as e:
                print(f"Error en verificación: {e}")
                firma_valida = False

        # 4. Preparar datos para mostrar (indicar estado de verificación)
        reserva_mostrar = {
            **datos_verificacion,
            'precio': precio_formateado,
            'verificado': firma_valida if firma_valida is not None else "No verificable"
        }

        # 5. Mostrar ticket
        app.cambiar_pantalla("ticket_vuelo", 
                               reserva_detalles=reserva_mostrar,
                               mostrar_guardar=False)

     except Exception as e:
        messagebox.showerror(
            "Error al mostrar ticket",
            f"Ocurrió un problema:\n{str(e)}"
        )

    cargar_reservas()
    
# Botón de "Regresar"
    btn_regresar = tk.Button(frame, text="Regresar al Inicio", font=("Arial", 12, "bold"),
                             bg="#6C757D", fg="white", relief="flat", width=20, cursor="hand2",
                             command=lambda: app.cambiar_pantalla("inicio"))
    btn_regresar.pack(pady=20)

    return frame


    
 def crear_pantalla_recuperar_contrasena(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="lightblue")

    btn_regresar = tk.Button(frame, text="←", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="lightblue", fg="blue", relief="flat", font=("Arial", 20), cursor="hand2")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Contenedor principal
    container = tk.Frame(frame, bg="white", bd=4, relief="groove")
    container.pack(pady=100, padx=50, ipadx=20, ipady=20)

    tk.Label(container, text="Recuperar Contraseña", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
    
    tk.Label(container, text="Correo Electrónico:", font=("Arial", 12), bg="white").pack(pady=5)
    correo_entry = tk.Entry(container, font=("Arial", 12), bd=2, relief="solid", width=25)
    correo_entry.pack(pady=5)

    # Campo oculto para nueva contraseña
    nueva_contrasena_label = tk.Label(container, text="Nueva Contraseña:", font=("Arial", 12), bg="white")
    nueva_contrasena_entry = tk.Entry(container, font=("Arial", 12), bd=2, relief="solid", width=25, show="*")

    # Botón de actualizar contraseña (inicialmente deshabilitado)
    btn_actualizar = tk.Button(container, text="Actualizar Contraseña", font=("Arial", 12, "bold"), bg="green", fg="white", relief="flat", width=20, cursor="hand2", state=tk.DISABLED)

    def verificar_correo():
        correo = correo_entry.get().strip()  # Elimina espacios extra
        if not correo:
            messagebox.showerror("Error", "Por favor, ingrese su correo electrónico.")
            return
        
        # Conectar con la base de datos para verificar si el correo existe
        conn = sqlite3.connect("base_de_datos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            messagebox.showinfo("Éxito", "Correo encontrado. Se enviará la contraseña a su correo.")
            
            # Enviar la contraseña al usuario
            recuperar_contrasena(correo)  # Se llama a la función para enviar el correo
            
            nueva_contrasena_label.pack(pady=5)
            nueva_contrasena_entry.pack(pady=5)
            btn_actualizar.pack(pady=10)
            btn_actualizar["state"] = tk.NORMAL  # Habilitar botón
        else:
            messagebox.showerror("Error", "El correo no está registrado.")

    def actualizar_contrasena():
        correo = correo_entry.get().strip()
        nueva_contrasena = nueva_contrasena_entry.get().strip()
        
        if not nueva_contrasena:
            messagebox.showerror("Error", "Ingrese una nueva contraseña.")
            return
        
        # Cifrar la nueva contraseña antes de guardarla
        nueva_contrasena_cifrada = cifrar_cesar(nueva_contrasena)

        # Actualizar la contraseña en la base de datos
        conn = sqlite3.connect("base_de_datos.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contrasena = ? WHERE correo = ?", (nueva_contrasena_cifrada, correo))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")

        # Limpiar los campos después de actualizar
        correo_entry.delete(0, tk.END)
        nueva_contrasena_entry.delete(0, tk.END)

        # Ocultar el campo de nueva contraseña y el botón de actualizar
        nueva_contrasena_label.pack_forget()
        nueva_contrasena_entry.pack_forget()
        btn_actualizar.pack_forget()

        app.cambiar_pantalla("login")  # Volver a la pantalla de inicio de sesión

    btn_verificar = tk.Button(container, text="Verificar Correo", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", relief="flat", width=20, cursor="hand2", command=verificar_correo)
    btn_verificar.pack(pady=10)

    btn_actualizar.config(command=actualizar_contrasena)

    return frame


 def crear_pantalla_registro(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="lightblue")  # Fondo azul claro

    btn_regresar = tk.Button(frame, text="←", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="lightblue", fg="blue", relief="flat", font=("Arial", 20), cursor="hand2")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Contenedor principal con el borde
    container = tk.Frame(frame, bg="white", bd=4, relief="groove")
    container.pack(pady=10, padx=50, ipadx=20, ipady=20)

    tk.Label(container, text="Registro de Usuario", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

    # Campos del formulario
    campos = ["Nombre completo", "Correo", "Usuario", "Contraseña", "Confirmar Contraseña"]
    entradas = {}

    for campo in campos:
        tk.Label(container, text=f"{campo}:", font=("Arial", 12), bg="white").pack(pady=5)
        if "Contraseña" in campo:
            entry = tk.Entry(container, font=("Arial", 12), show="*", bd=2, relief="solid", width=25)
        else:
            entry = tk.Entry(container, font=("Arial", 12), bd=2, relief="solid", width=25)
        entry.pack(pady=5)
        entradas[campo] = entry  # Guarda las entradas en un diccionario

    def validar_correo(correo):
        """Valida que el correo tenga un formato correcto"""
        return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", correo)

    def validar_contrasena(contrasena):
        """Verifica que la contraseña tenga al menos 8 caracteres y solo contenga letras (sin números ni caracteres especiales)"""
        return len(contrasena) >= 8 and contrasena.isalpha()

    def validar_nombre(nombre):
        """Valida que el nombre completo tenga al menos un nombre y dos apellidos"""
        partes = nombre.split()
        if len(partes) >= 3:
            return True
        return False

    def registrar_usuario():
        nombre = entradas["Nombre completo"].get().strip()
        correo = entradas["Correo"].get().strip()
        usuario = entradas["Usuario"].get().strip()
        contrasena = entradas["Contraseña"].get().strip()
        confirmar_contrasena = entradas["Confirmar Contraseña"].get().strip()

        if not all([nombre, correo, usuario, contrasena, confirmar_contrasena]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Error", "El correo ingresado no es válido.")
            return

        if not validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre completo debe tener al menos un nombre y dos apellidos.")
            return

        if len(usuario) < 4:
            messagebox.showerror("Error", "El nombre de usuario debe tener al menos 4 caracteres.")
            return

        if not validar_contrasena(contrasena):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula a excepción de números.")
            return

        if contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        contrasena_cifrada = cifrar_cesar(contrasena)  # Cifra la contraseña antes de guardarla

        # Conectar a la base de datos
        conn = sqlite3.connect("base_de_datos.db")
        cursor = conn.cursor()

        # Crear la tabla si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT UNIQUE,
            usuario TEXT UNIQUE,
            contrasena TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cupones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            descuento INTEGER NOT NULL,
            usado BOOLEAN DEFAULT 0,
            id_usuario INTEGER,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
        """)

        try:
            # Insertar los datos del usuario en la base de datos
            cursor.execute("""
            INSERT INTO usuarios (nombre, correo, usuario, contrasena)
            VALUES (?, ?, ?, ?)
            """, (nombre, correo, usuario, contrasena_cifrada))

            # Obtener el id del usuario recién insertado
            user_id = cursor.lastrowid

            # Insertar 3 cupones para el usuario recién registrado
            cupones = [
                ("DESCUENTO10", 10, 0),  # Primer cupón
                ("DESCUENTO20", 20, 0),  # Segundo cupón
                ("DESCUENTO30", 30, 0)   # Tercer cupón
            ]
            for codigo_cupon, descuento, usado in cupones:
                cursor.execute("""
                INSERT INTO cupones (codigo, descuento, usado, id_usuario)
                VALUES (?, ?, ?, ?)
                """, (codigo_cupon, descuento, usado, user_id))

            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente y cupones asignados.")

            # Limpiar los campos después de registrar
            for campo in entradas.values():
                campo.delete(0, tk.END)

            app.cambiar_pantalla("login")

        except sqlite3.OperationalError as e:
            # Si hay un bloqueo, muestra un mensaje de error
            messagebox.showerror("Error", f"Hubo un error al registrar el usuario: {e}")
            conn.rollback()  # Realiza un rollback en caso de error

        finally:
            conn.close()  # Asegúrate de cerrar la conexión

    btn_registrar = tk.Button(container, text="Registrar", font=("Arial", 12, "bold"), bg="#007BFF", fg="white",
                               relief="flat", width=20, cursor="hand2", command=registrar_usuario)
    btn_registrar.pack(pady=10)

    return frame
    
    
    
 def crear_pantalla_nosotros(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")  # Fondo azul claro

    # Botón de regresar con estilo
    btn_regresar = tk.Button(frame, text="← Volver", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="#007BFF", fg="white", relief="flat", font=("Arial", 16, "bold"), cursor="hand2",
                             activebackground="#0056b3", activeforeground="white")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Contenedor con scroll oculto por defecto
    canvas = tk.Canvas(frame, bg="#ADD8E6", highlightthickness=0)  
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
    scrollable_frame = tk.Frame(canvas, bg="#ADD8E6")
    
    # Función para mostrar/ocultar el scroll
    def actualizar_scroll(event=None):
        """Muestra el scroll solo si el contenido es más grande que la pantalla"""
        canvas.update_idletasks()  # Asegura que los widgets ya estén dibujados
        canvas.configure(scrollregion=canvas.bbox("all"))  
        
        if scrollable_frame.winfo_reqheight() > frame.winfo_height():
            scrollbar.pack(side="right", fill="y")  # Muestra el scroll si el contenido es mayor
        else:
            scrollbar.pack_forget()  # Oculta el scroll si no es necesario

    scrollable_frame.bind("<Configure>", actualizar_scroll)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)

    # Título sin contenedor adicional
    tk.Label(scrollable_frame, text="Descubre más sobre Aerotrip", 
             font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#003366").pack(pady=20)

    # Texto de presentación sin caja blanca
    texto = """
Nuestra aplicación Aerotrip busca revolucionar la forma en que los usuarios gestionan sus vuelos. 
Con un enfoque en la simplicidad, accesibilidad y personalización, Aerotrip ofrece una plataforma intuitiva 
para reservar y administrar vuelos de manera eficiente.

A través de su interfaz amigable, los usuarios pueden:
✔ Buscar vuelos en tiempo real.
✔ Realizar pagos seguros y rápidos.

Nuestro compromiso es proporcionar una experiencia de usuario óptima, respaldada por tecnología avanzada 
que asegura la protección de los datos personales y financieros de nuestros usuarios.
"""
    tk.Label(scrollable_frame, text=texto, font=("Arial", 14), bg="#ADD8E6", fg="black",
             wraplength=900, justify="center", padx=20).pack(pady=10)

    # Ejecutar la función después de que la pantalla se haya mostrado
    frame.after(100, actualizar_scroll)

    return frame


 def crear_pantalla_aviso_privacidad(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")  # Fondo azul claro

    # Botón de regresar con estilo
    btn_regresar = tk.Button(frame, text="← Volver", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="#007BFF", fg="white", relief="flat", font=("Arial", 16, "bold"), cursor="hand2",
                             activebackground="#0056b3", activeforeground="white")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Canvas para manejar el scroll
    canvas = tk.Canvas(frame, bg="#ADD8E6", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
    scrollable_frame = tk.Frame(canvas, bg="#ADD8E6")
    
    # Actualizar la región del canvas cuando el contenido cambia
    def actualizar_scroll():
        canvas.update_idletasks()  # Asegura que los widgets ya estén dibujados
        canvas.configure(scrollregion=canvas.bbox("all"))  # Ajusta la región del scroll
        
        # Si el contenido es mayor que la pantalla, muestra el scroll
        if scrollable_frame.winfo_reqheight() > frame.winfo_height():
            scrollbar.pack(side="right", fill="y")  # Muestra el scroll
        else:
            scrollbar.pack_forget()  # Oculta el scroll si no es necesario

    scrollable_frame.bind("<Configure>", lambda e: actualizar_scroll())  # Actualiza el scroll al configurar el contenido
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  # Pone el frame dentro del canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y", padx=5)

    # Título sin contenedor adicional
    tk.Label(scrollable_frame, text="Aviso de Privacidad", 
             font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#003366").pack(pady=20)

    # Texto de aviso de privacidad sin caja blanca
    texto = """
    Última actualización: 24 de marzo de 2025  

    En Aerotrip, la privacidad y seguridad de nuestros usuarios es nuestra prioridad. Este Aviso de Privacidad explica qué información recopilamos, cómo la utilizamos y qué medidas tomamos para protegerla.

    1. Información que recopilamos:
       - Datos de registro: Nombre y correo electrónico.
       - Información de viajes: Historial de reservas y preferencias de vuelo.
       - Datos financieros: Información necesaria para procesar pagos de reservas.

    2. Uso de la información:
       - Procesar y gestionar tus reservas de vuelos.
       - Mejorar la experiencia de usuario dentro de nuestra aplicación.
       - Enviarte notificaciones relevantes sobre tus vuelos y promociones.

    3. Protección de la información:
       - Implementamos medidas de seguridad avanzadas, incluyendo cifrado de datos, servidores protegidos y protocolos de autenticación.

    4. Compartición de datos:
       - En Aerotrip, garantizamos que no vendemos ni compartimos tu información personal con terceros, salvo en los siguientes casos:
         - Cuando sea requerido por autoridades legales.
         - Con proveedores de pago para procesar transacciones de manera segura.

    5. Modificaciones a este Aviso:
       - Podemos actualizar este Aviso de Privacidad en cualquier momento. Te notificaremos cualquier cambio mediante la fecha de actualización en esta página.
    """
    
    tk.Label(scrollable_frame, text=texto, font=("Arial", 14), bg="#ADD8E6", fg="black",
             wraplength=900, justify="left", padx=20).pack(pady=10)

    # Función para permitir el desplazamiento con el mouse
    def desplazamiento_con_mouse(event):
        """Permite el desplazamiento con la rueda del mouse"""
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Asociar el desplazamiento con el mouse
    frame.bind_all("<MouseWheel>", desplazamiento_con_mouse)

    # Ejecutar la función después de que la pantalla se haya mostrado
    frame.after(100, actualizar_scroll)

    return frame


 def crear_pantalla_acuerdo_confidencialidad(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")  # Fondo azul claro

    # Botón de regresar con estilo
    btn_regresar = tk.Button(frame, text="← Volver", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="#007BFF", fg="white", relief="flat", font=("Arial", 16, "bold"), cursor="hand2",
                             activebackground="#0056b3", activeforeground="white")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Contenedor con scroll oculto por defecto
    canvas = tk.Canvas(frame, bg="#ADD8E6", highlightthickness=0)  
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
    scrollable_frame = tk.Frame(canvas, bg="#ADD8E6")
    
    # Función para mostrar/ocultar el scroll
    def actualizar_scroll(event=None):
        """Muestra el scroll solo si el contenido es más grande que la pantalla"""
        canvas.update_idletasks()  # Asegura que los widgets ya estén dibujados
        canvas.configure(scrollregion=canvas.bbox("all"))  
        
        if scrollable_frame.winfo_reqheight() > frame.winfo_height():
            scrollbar.pack(side="right", fill="y")  # Muestra el scroll si el contenido es mayor
        else:
            scrollbar.pack_forget()  # Oculta el scroll si no es necesario

    scrollable_frame.bind("<Configure>", actualizar_scroll)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)

    # Título sin contenedor adicional
    tk.Label(scrollable_frame, text="Acuerdo de Confidencialidad", 
             font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#003366").pack(pady=20)

    # Texto de acuerdo de confidencialidad sin caja blanca
    texto = """
    Última actualización: 24 de marzo de 2025 

    1. Objeto del Acuerdo
       Este Acuerdo tiene como finalidad proteger la información confidencial proporcionada por el Usuario o generada a través del uso de la aplicación. Esta incluye datos personales, financieros y relacionados con las reservas de vuelos.

    2. Información Confidencial
       Se considera información confidencial la siguiente:
       - Datos personales del Usuario: Nombre, correo electrónico y detalles de vuelos.
       - Información financiera: Datos de tarjetas de crédito o débito, recolectados solo para procesar transacciones.

    3. Obligaciones de Confidencialidad
       - Aerotrip se compromete a no divulgar, compartir o vender la información confidencial del Usuario, salvo en los casos establecidos en el Aviso de Privacidad o cuando sea requerido por ley.
       - Aerotrip implementará las medidas necesarias para proteger la confidencialidad de la información del Usuario, utilizando cifrado y almacenando los datos en servidores seguros.

    4. Exclusiones
       Este acuerdo no aplicará en los siguientes casos:
       - Cuando la información sea pública o se haya hecho pública por un tercero sin restricciones.
       - Cuando la información haya sido divulgada por el Usuario de forma voluntaria.
       - Cuando la información sea solicitada por autoridad judicial o gubernamental, de acuerdo con la ley.

    5. Duración del Acuerdo
       Este Acuerdo de Confidencialidad será válido durante todo el período de uso de la aplicación y por un período adicional de 5 años a partir de la última interacción del Usuario con Aerotrip.

    6. Consecuencias de la Violación
       En caso de violación a este acuerdo:
       - Se tomarán acciones correctivas inmediatas, incluyendo la eliminación de los datos, si es necesario.
       - La cuenta del Usuario podrá ser cancelada si se viola el acuerdo, como por ejemplo, la divulgación no autorizada de información confidencial.
       - Aerotrip se reserva el derecho de tomar acciones legales si la seguridad de los datos del Usuario se ve comprometida.

    7. Jurisdicción y Resolución de Conflictos
       Este acuerdo se rige por las leyes de México. En caso de disputa, ambas partes se someten a la jurisdicción de los tribunales competentes en la Ciudad de México.
    """
    tk.Label(scrollable_frame, text=texto, font=("Arial", 14), bg="#ADD8E6", fg="black",
             wraplength=900, justify="left", padx=20).pack(pady=10)

    # Función para permitir el desplazamiento con el mouse
    frame.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    # Ejecutar la función después de que la pantalla se haya mostrado
    frame.after(100, actualizar_scroll)

    return frame

 def crear_pantalla_terminos_uso(app):
    frame = tk.Frame(app.contenedor_pantallas, bg="#ADD8E6")  # Fondo azul claro

    # Botón de regresar con estilo
    btn_regresar = tk.Button(frame, text="← Volver", command=lambda: app.cambiar_pantalla("inicio"),
                             bg="#007BFF", fg="white", relief="flat", font=("Arial", 16, "bold"), cursor="hand2",
                             activebackground="#0056b3", activeforeground="white")
    btn_regresar.pack(anchor="w", padx=20, pady=10)

    # Contenedor con scroll oculto por defecto
    canvas = tk.Canvas(frame, bg="#ADD8E6", highlightthickness=0)  
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
    scrollable_frame = tk.Frame(canvas, bg="#ADD8E6")
    
    # Función para mostrar/ocultar el scroll
    def actualizar_scroll(event=None):
        """Muestra el scroll solo si el contenido es más grande que la pantalla"""
        canvas.update_idletasks()  # Asegura que los widgets ya estén dibujados
        canvas.configure(scrollregion=canvas.bbox("all"))  
        
        if scrollable_frame.winfo_reqheight() > frame.winfo_height():
            scrollbar.pack(side="right", fill="y")  # Muestra el scroll si el contenido es mayor
        else:
            scrollbar.pack_forget()  # Oculta el scroll si no es necesario

    scrollable_frame.bind("<Configure>", actualizar_scroll)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)

    # Título sin contenedor adicional
    tk.Label(scrollable_frame, text="Términos y Condiciones de Uso", 
             font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#003366").pack(pady=20)

    # Texto de términos y condiciones sin caja blanca
    texto = """

    Última actualización: 24 de marzo de 2025 

    1. Licencia de Uso
       Al utilizar la aplicación Aerotrip, el Usuario acepta los términos relacionados con el uso del software proporcionado dentro de la plataforma. Aerotrip se compromete a garantizar que las tecnologías utilizadas sean seguras y cumplan con los estándares de la industria para proteger los datos y la privacidad de los usuarios. La aplicación se ha desarrollado utilizando **Python** como el lenguaje principal, junto con bibliotecas y tecnologías como **Tkinter** para la interfaz gráfica de usuario (GUI), garantizando un rendimiento estable y fácil de usar en diversas plataformas.

    2. Tecnologías Empleadas
       **Python** es el lenguaje de programación base para Aerotrip, con el cual hemos desarrollado todas las funcionalidades principales de la aplicación. Además, se emplean las siguientes tecnologías para asegurar una experiencia eficiente:
       - **Tkinter**: Utilizado para crear la interfaz gráfica de usuario (GUI) de la aplicación.
       - **SQLite**: Para el almacenamiento de datos de manera local y eficiente.

       Estas tecnologías garantizan una experiencia fluida, segura y de alta calidad para los usuarios.

    3. Responsabilidad del Usuario
       El Usuario se compromete a no realizar las siguientes acciones:
       • Usar el software con fines ilícitos o contrarios a los términos establecidos en este acuerdo.
       • Modificar, descompilar o realizar ingeniería inversa sobre el software de la aplicación.
       • Introducir código malicioso, virus o malware que afecte el funcionamiento seguro de la aplicación.

    4. Actualizaciones del Software
       Aerotrip se compromete a mantener actualizado el software de la aplicación para mejorar la experiencia del usuario y garantizar la seguridad de los datos. Las actualizaciones estarán disponibles de manera periódica para asegurar que los usuarios siempre tengan acceso a las últimas funcionalidades y mejoras. 

       El proceso de actualización será transparente para el usuario y no obligará a realizar cambios manuales, dado que el sistema estará diseñado para ser autónomo en cuanto a actualizaciones.

    5. Duración de la Licencia
       La licencia de uso de la aplicación es gratuita, pero puede ser suspendida o revocada si el Usuario incumple los términos de uso establecidos en este acuerdo. Aerotrip se reserva el derecho de modificar o finalizar el acceso del Usuario a la plataforma si no cumple con las condiciones de uso de la misma.

    """
    tk.Label(scrollable_frame, text=texto, font=("Arial", 14), bg="#ADD8E6", fg="black",
             wraplength=900, justify="left", padx=20).pack(pady=10)

    # Función para permitir el desplazamiento con el mouse
    frame.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    # Ejecutar la función después de que la pantalla se haya mostrado
    frame.after(100, actualizar_scroll)

    return frame

 def _crear_pantalla_texto(app, titulo, texto):
        frame = tk.Frame(app.contenedor_pantallas, bg="white")
        btn_regresar = tk.Button(frame, text="←", command=lambda: app.cambiar_pantalla("inicio"),
                                 bg="white", fg="blue", relief="flat", font=("Arial", 20), cursor="hand2")
        btn_regresar.pack(anchor="w", padx=20, pady=10)
        tk.Label(frame, text=titulo, font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        texto_area = scrolledtext.ScrolledText(frame, width=100, height=30, font=("Arial", 14), wrap=tk.WORD)
        texto_area.insert(tk.END, texto)
        texto_area.configure(state="disabled")
        texto_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        return frame