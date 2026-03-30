import customtkinter as ctk
import os
from PIL import Image

class PantallaMenuPrincipal(ctk.CTkToplevel):
    # CORRECCIÓN 1: Añadimos 'on_abrir_bd=None' a los parámetros
    def __init__(self, on_abrir_botellas=None, on_abrir_usuarios=None, on_abrir_bd=None):
        super().__init__()
        
        # Callbacks para cuando hagamos clic en los botones
        self.on_abrir_botellas = on_abrir_botellas
        self.on_abrir_usuarios = on_abrir_usuarios
        self.on_abrir_bd = on_abrir_bd # Guardamos la variable
        
        self.title("Panel Central - Milcast Corp")
        self.geometry("650x550")
        self.resizable(False, False)

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=20, pady=20)

        # Cargar Logo
        ruta_actual = os.path.dirname(__file__)
        ruta_logo = os.path.join(ruta_actual, "..", "Aranjuez_logo.png") 
        
        try:
            pil_image = Image.open(ruta_logo)
            self.ctk_logo = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(80, 80))
            self.label_logo = ctk.CTkLabel(self.header_frame, text="", image=self.ctk_logo)
        except:
            self.label_logo = ctk.CTkLabel(self.header_frame, text="[ LOGO ]", width=80, height=80, fg_color="gray30")
        
        self.label_logo.pack(side="left", padx=(0, 20))

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="MENÚ PRINCIPAL", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(side="left")

        # --- CUERPO (CUADRÍCULA DE BOTONES) ---
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=(20, 10))

        ancho_btn = 160
        alto_btn = 140
        fuente_btn = ("Roboto", 16, "bold")

        self.btn_usuarios = ctk.CTkButton(self.grid_frame, text="👤\n\nUsuarios", width=ancho_btn, height=alto_btn, 
                                          font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.btn_usuarios_click)
        self.btn_usuarios.grid(row=0, column=0, padx=15, pady=15)

        self.btn_botellas = ctk.CTkButton(self.grid_frame, text="🍾\n\nTipo de Botella", width=ancho_btn, height=alto_btn, 
                                          font=fuente_btn, fg_color="#1f538d", hover_color="#14375e", command=self.btn_botellas_click)
        self.btn_botellas.grid(row=0, column=1, padx=15, pady=15)

        self.btn_bd = ctk.CTkButton(self.grid_frame, text="📊\n\nBase de Datos", width=ancho_btn, height=alto_btn, 
                                    font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", 
                                    command=self.btn_bd_click) 
        # CORRECCIÓN 2: Faltaba esta línea para mostrar el botón en pantalla
        self.btn_bd.grid(row=1, column=0, padx=15, pady=15)

        self.btn_opcion1 = ctk.CTkButton(self.grid_frame, text="⚙️\n\nOpción 1", width=ancho_btn, height=alto_btn, 
                                         font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.en_construccion)
        self.btn_opcion1.grid(row=1, column=1, padx=15, pady=15)

    def btn_usuarios_click(self):
        if self.on_abrir_usuarios:
            self.on_abrir_usuarios()
        else:
            print("Módulo Usuarios no conectado")

    def btn_botellas_click(self):
        if self.on_abrir_botellas:
            self.on_abrir_botellas()
        else:
            print("Módulo Botellas no conectado")

    def en_construccion(self):
        print("Este módulo aún está en desarrollo.")

    # CORRECCIÓN 3: Indentación correcta (espacios a la izquierda)
    def btn_bd_click(self):
        if hasattr(self, 'on_abrir_bd') and self.on_abrir_bd:
            self.on_abrir_bd()
        else:
            print("Módulo BD no conectado")