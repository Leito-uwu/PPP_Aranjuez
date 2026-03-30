import customtkinter as ctk
import os
from PIL import Image
from tkinter import ttk 
from Base_Datos.gestor_produccion import obtener_registros, registrar_botella
import random

class PantallaBaseDatos(ctk.CTkToplevel):
    # 🟢 AÑADIMOS formato_actual
    def __init__(self, on_volver, formato_actual):
        super().__init__()
        self.on_volver = on_volver
        self.formato_actual = formato_actual # Guardamos el formato que nos manda main.py
        
        self.title("Reporte de Producción - Milcast Corp")
        self.geometry("700x550")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=20, pady=20)

        ruta_logo = os.path.join(os.path.dirname(__file__), "..", "Aranjuez_logo.png")
        try:
            pil_image = Image.open(ruta_logo)
            self.ctk_logo = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(80, 80))
            self.label_logo = ctk.CTkLabel(self.header_frame, text="", image=self.ctk_logo)
        except:
            self.label_logo = ctk.CTkLabel(self.header_frame, text="[ LOGO ]", width=80, height=80, fg_color="gray30")
        self.label_logo.pack(side="left", padx=(0, 20))

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="BASE DE DATOS (SCADA)", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(side="left")

        self.btn_volver = ctk.CTkButton(self.header_frame, text="Volver al Menú", width=100, 
                                        fg_color="gray40", hover_color="gray30", command=self.cerrar_ventana)
        self.btn_volver.pack(side="right")

        self.separador = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=(0, 10))

        # --- TABLA DE DATOS ---
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b")
        estilo.map('Treeview', background=[('selected', '#1f538d')])
        estilo.configure("Treeview.Heading", background="#1f538d", foreground="white", font=('Roboto', 12, 'bold'))

        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("Fecha", "Formato", "Buenas", "Malas")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=8)
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=150)
            
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # --- PANEL DE SIMULACIÓN Y CONTROL ---
        self.frame_controles = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controles.pack(fill="x", padx=20, pady=(0, 20))

        self.btn_actualizar = ctk.CTkButton(self.frame_controles, text="🔄 Actualizar Tabla", command=self.cargar_datos)
        self.btn_actualizar.pack(side="left", padx=10)

        # 🟢 CAMBIAMOS EL TEXTO DEL BOTÓN PARA QUE MUESTRE QUÉ BOTELLA ESTÁ SIMULANDO
        texto_boton = f"⚙️ Simular 10 ({self.formato_actual})"
        self.btn_simular = ctk.CTkButton(self.frame_controles, text=texto_boton, 
                                         fg_color="#ff9800", hover_color="#e65100", command=self.simular_ingreso)
        self.btn_simular.pack(side="right", padx=10)

        self.cargar_datos()

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        registros = obtener_registros()
        for registro in registros:
            self.tabla.insert("", "end", values=registro)

    def simular_ingreso(self):
        estados = ["BUENA", "BUENA", "BUENA", "BUENA", "MALA"] 
        
        for _ in range(10):
            estado_elegido = random.choice(estados)
            # 🟢 AQUÍ USAMOS LA VARIABLE GLOBAL EN VEZ DE AZAR
            registrar_botella(self.formato_actual, estado_elegido)
            
        print(f"Simuladas 10 unidades de {self.formato_actual}")
        self.cargar_datos() 

    def cerrar_ventana(self):
        self.destroy()
        self.on_volver()