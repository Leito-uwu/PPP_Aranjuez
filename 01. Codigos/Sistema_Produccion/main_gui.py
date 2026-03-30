import customtkinter as ctk

# ==========================================
# CONFIGURACIÓN GENERAL DE LA INTERFAZ
# ==========================================
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

# ==========================================
# 3. PANTALLA DE INSPECCIÓN (TIPO DE BOTELLA)
# ==========================================
class PantallaInspeccion(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Configuración de Botellas - Milcast Corp")
        self.geometry("600x450")
        self.resizable(False, False)
        
        self.parent = parent # Guardamos referencia al Menú Principal
        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu) 

        # --- CABECERA (TÍTULO Y BOTÓN VOLVER) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=20, pady=20)

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="CONFIGURACIÓN DE LÍNEA", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(side="left")

        # Botón para volver al menú anterior
        self.btn_volver = ctk.CTkButton(self.header_frame, text="Volver al Menú", width=100, 
                                        fg_color="gray40", hover_color="gray30", command=self.volver_al_menu)
        self.btn_volver.pack(side="right")

        # --- CUERPO DEL PANEL ---
        self.separador = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=(0, 20))

        self.label_instruccion = ctk.CTkLabel(self, text="Seleccione el formato de botella a inspeccionar:", 
                                              font=("Roboto", 14), text_color="gray")
        self.label_instruccion.pack(pady=(10, 20))

        opciones_botellas = ["Botella Tipo A", "Botella Tipo B", "Botella Tipo C", "Botella Tipo D", "Botella Tipo E"]
        self.selector_formato = ctk.CTkOptionMenu(self, values=opciones_botellas, command=self.al_cambiar_formato, 
                                                  width=250, height=40, font=("Roboto", 14))
        self.selector_formato.pack(pady=10)

        self.label_estado = ctk.CTkLabel(self, text="Formato actual: Botella Tipo A", font=("Roboto", 16), text_color="yellow")
        self.label_estado.pack(pady=20)

        self.btn_arrancar = ctk.CTkButton(self, text="ARRANCAR INSPECCIÓN", width=250, height=50, 
                                          font=("Roboto", 16, "bold"), fg_color="green", hover_color="darkgreen")
        self.btn_arrancar.pack(pady=30)

    def al_cambiar_formato(self, eleccion):
        self.label_estado.configure(text=f"Formato actual: {eleccion}")

    def volver_al_menu(self):
        self.destroy()          # Cierra esta ventana
        self.parent.deiconify() # Vuelve a hacer visible el Menú Principal


# ==========================================
# 2. PANEL CENTRAL (DASHBOARD CON LOS 4 CUADRADOS)
# ==========================================
class PantallaMenuPrincipal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Panel Central - Milcast Corp")
        self.geometry("550x500")
        self.resizable(False, False)
        
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sistema)

        self.label_titulo = ctk.CTkLabel(self, text="MENÚ PRINCIPAL", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=(30, 20))

        # Contenedor para la cuadrícula (Grid) de botones
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=10)

        # Configuramos el tamaño de los "cuadrados"
        ancho_btn = 160
        alto_btn = 140
        fuente_btn = ("Roboto", 16, "bold")

        # --- LOS 4 BOTONES CUADRADOS ---
        # 1. Usuarios (Fila 0, Columna 0)
        self.btn_usuarios = ctk.CTkButton(self.grid_frame, text="Usuarios", width=ancho_btn, height=alto_btn, 
                                          font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.en_construccion)
        self.btn_usuarios.grid(row=0, column=0, padx=15, pady=15)

        # 2. Tipo de Botella (Fila 0, Columna 1) -> ¡ESTE ES EL QUE FUNCIONA!
        self.btn_botellas = ctk.CTkButton(self.grid_frame, text="Tipo de Botella", width=ancho_btn, height=alto_btn, 
                                          font=fuente_btn, fg_color="#1f538d", hover_color="#14375e", command=self.abrir_inspeccion)
        self.btn_botellas.grid(row=0, column=1, padx=15, pady=15)

        # 3. Base de Datos (Fila 1, Columna 0)
        self.btn_bd = ctk.CTkButton(self.grid_frame, text="Base de Datos", width=ancho_btn, height=alto_btn, 
                                    font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.en_construccion)
        self.btn_bd.grid(row=1, column=0, padx=15, pady=15)

        # 4. Opción 1 (Fila 1, Columna 1)
        self.btn_opcion1 = ctk.CTkButton(self.grid_frame, text="Opción 1", width=ancho_btn, height=alto_btn, 
                                         font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.en_construccion)
        self.btn_opcion1.grid(row=1, column=1, padx=15, pady=15)

    def abrir_inspeccion(self):
        self.withdraw() # Oculta el menú principal
        ventana_inspeccion = PantallaInspeccion(self)
        ventana_inspeccion.focus()

    def en_construccion(self):
        print("Este módulo aún está en desarrollo.")

    def cerrar_sistema(self):
        self.parent.destroy() # Cierra todo el programa si le dan a la X

# ==========================================
# 1. VENTANA DE LOGIN (PANTALLA DE INICIO)
# ==========================================
class PantallaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Milcast Corp - Acceso")
        self.geometry("400x450")
        self.resizable(False, False) 
        
        self.label_titulo = ctk.CTkLabel(self, text="SISTEMA DE INSPECCIÓN", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(pady=(50, 5))
        
        self.label_subtitulo = ctk.CTkLabel(self, text="Identificación de Operador", font=("Roboto", 14), text_color="gray")
        self.label_subtitulo.pack(pady=(0, 40))
        
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="ID de Operador", width=250, height=40, justify="center")
        self.entry_usuario.pack(pady=10)
        
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250, height=40, justify="center")
        self.entry_password.pack(pady=10)
        
        self.label_mensaje = ctk.CTkLabel(self, text="", font=("Roboto", 12))
        self.label_mensaje.pack(pady=5)
        
        self.btn_ingresar = ctk.CTkButton(self, text="INICIAR SESIÓN", width=250, height=40, font=("Roboto", 14, "bold"), command=self.validar_acceso)
        self.btn_ingresar.pack(pady=20)
        
    def validar_acceso(self):
        # Credenciales correctas: admin / 1234
        if self.entry_usuario.get() == "admin" and self.entry_password.get() == "1234":
            self.withdraw() # Oculta la ventana de Login
            ventana_menu = PantallaMenuPrincipal(self)
            ventana_menu.focus() 
        else:
            self.label_mensaje.configure(text="❌ ID o Contraseña incorrectos", text_color="red")

# ==========================================
# ARRANQUE DEL PROGRAMA
# ==========================================
if __name__ == "__main__":
    app = PantallaLogin()
    app.mainloop()