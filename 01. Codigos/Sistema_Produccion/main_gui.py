import customtkinter as ctk
import os
import json
from PIL import Image 

# ==========================================
# FUNCIONES DE BASE DE DATOS (JSON)
# ==========================================
def obtener_ruta_bd():
    ruta_script = os.path.dirname(__file__)
    return os.path.join(ruta_script, "usuarios.json")

def cargar_usuarios():
    ruta_bd = obtener_ruta_bd()
    # Si el archivo no existe, creamos el administrador por defecto
    if not os.path.exists(ruta_bd):
        usuarios_por_defecto = {"admin": "1234"}
        guardar_usuarios(usuarios_por_defecto)
        return usuarios_por_defecto
    
    with open(ruta_bd, "r") as archivo:
        return json.load(archivo)

def guardar_usuarios(diccionario_usuarios):
    ruta_bd = obtener_ruta_bd()
    with open(ruta_bd, "w") as archivo:
        json.dump(diccionario_usuarios, archivo, indent=4)


# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

# ==========================================
# 4. PANTALLA DE GESTIÓN DE USUARIOS
# ==========================================
class PantallaUsuarios(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Usuarios - Milcast Corp")
        self.geometry("650x500")
        self.resizable(False, False)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu)

        # --- CABECERA (LOGO, TÍTULO Y BOTÓN VOLVER) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=20, pady=20)

        ruta_logo = os.path.join(os.path.dirname(__file__), "Aranjuez_logo.png")
        try:
            pil_image = Image.open(ruta_logo)
            self.ctk_logo = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(80, 80))
            self.label_logo = ctk.CTkLabel(self.header_frame, text="", image=self.ctk_logo)
        except:
            self.label_logo = ctk.CTkLabel(self.header_frame, text="[ LOGO ]", width=80, height=80, fg_color="gray30")
        self.label_logo.pack(side="left", padx=(0, 20))

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="GESTIÓN DE USUARIOS", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(side="left")

        self.btn_volver = ctk.CTkButton(self.header_frame, text="Volver al Menú", width=100, 
                                        fg_color="gray40", hover_color="gray30", command=self.volver_al_menu)
        self.btn_volver.pack(side="right")

        self.separador = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=(0, 10))

        # --- CUERPO DIVIDIDO EN DOS (CREAR Y ELIMINAR) ---
        self.frame_izq = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_izq.pack(side="left", fill="both", expand=True, padx=20)
        
        self.frame_der = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_der.pack(side="right", fill="both", expand=True, padx=20)

        # --- SECCIÓN IZQUIERDA: CREAR USUARIO ---
        self.lbl_crear = ctk.CTkLabel(self.frame_izq, text="➕ Crear Nuevo Operador", font=("Roboto", 16, "bold"), text_color="#4CAF50")
        self.lbl_crear.pack(pady=10)

        self.entry_nuevo_id = ctk.CTkEntry(self.frame_izq, placeholder_text="Nuevo ID de Operador", width=200)
        self.entry_nuevo_id.pack(pady=10)

        self.entry_nueva_pass = ctk.CTkEntry(self.frame_izq, placeholder_text="Contraseña", width=200)
        self.entry_nueva_pass.pack(pady=10)

        self.btn_crear = ctk.CTkButton(self.frame_izq, text="Guardar Usuario", fg_color="green", hover_color="darkgreen", command=self.crear_usuario)
        self.btn_crear.pack(pady=15)

        # --- SECCIÓN DERECHA: ELIMINAR USUARIO ---
        self.lbl_eliminar = ctk.CTkLabel(self.frame_der, text="🗑️ Eliminar Operador", font=("Roboto", 16, "bold"), text_color="#F44336")
        self.lbl_eliminar.pack(pady=10)

        self.lbl_instruccion_eliminar = ctk.CTkLabel(self.frame_der, text="Seleccione el ID a eliminar:", font=("Roboto", 12))
        self.lbl_instruccion_eliminar.pack(pady=(10, 0))

        # Usamos un menú desplegable para evitar que borren usuarios por error tipográfico
        self.selector_eliminar = ctk.CTkOptionMenu(self.frame_der, values=["Cargando..."], width=200)
        self.selector_eliminar.pack(pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_der, text="Eliminar Usuario", fg_color="#d32f2f", hover_color="#9a0007", command=self.eliminar_usuario)
        self.btn_eliminar.pack(pady=15)

        # Mensajes del sistema
        self.lbl_mensaje = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.lbl_mensaje.pack(side="bottom", pady=20)

        # Cargar la lista al iniciar la ventana
        self.actualizar_lista_desplegable()

    def actualizar_lista_desplegable(self):
        usuarios_db = cargar_usuarios()
        lista_ids = list(usuarios_db.keys())
        self.selector_eliminar.configure(values=lista_ids)
        self.selector_eliminar.set(lista_ids[0] if lista_ids else "")

    def crear_usuario(self):
        nuevo_id = self.entry_nuevo_id.get().strip()
        nueva_pass = self.entry_nueva_pass.get().strip()

        if not nuevo_id or not nueva_pass:
            self.lbl_mensaje.configure(text="⚠️ Complete ambos campos", text_color="yellow")
            return

        usuarios_db = cargar_usuarios()
        if nuevo_id in usuarios_db:
            self.lbl_mensaje.configure(text="❌ El usuario ya existe", text_color="red")
        else:
            usuarios_db[nuevo_id] = nueva_pass
            guardar_usuarios(usuarios_db)
            self.actualizar_lista_desplegable()
            self.entry_nuevo_id.delete(0, 'end')
            self.entry_nueva_pass.delete(0, 'end')
            self.lbl_mensaje.configure(text=f"✅ Usuario '{nuevo_id}' creado exitosamente", text_color="green")

    def eliminar_usuario(self):
        id_a_eliminar = self.selector_eliminar.get()
        
        if id_a_eliminar == "admin":
            self.lbl_mensaje.configure(text="⛔ No puedes eliminar al administrador", text_color="red")
            return

        usuarios_db = cargar_usuarios()
        if id_a_eliminar in usuarios_db:
            del usuarios_db[id_a_eliminar]
            guardar_usuarios(usuarios_db)
            self.actualizar_lista_desplegable()
            self.lbl_mensaje.configure(text=f"🗑️ Usuario '{id_a_eliminar}' eliminado", text_color="yellow")

    def volver_al_menu(self):
        self.destroy()
        self.parent.deiconify()


# ==========================================
# 3. PANTALLA DE INSPECCIÓN (Igual que antes)
# ==========================================
class PantallaInspeccion(ctk.CTkToplevel):
    # ... (El código de la ventana de botellas se mantiene exactamente igual)
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuración de Botellas - Milcast Corp")
        self.geometry("650x500")
        self.resizable(False, False)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu) 
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=20, pady=20)
        ruta_script = os.path.dirname(__file__) 
        ruta_logo = os.path.join(ruta_script, "Aranjuez_logo.png")
        try:
            pil_image = Image.open(ruta_logo)
            self.ctk_logo = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(80, 80))
            self.label_logo = ctk.CTkLabel(self.header_frame, text="", image=self.ctk_logo)
        except:
            self.label_logo = ctk.CTkLabel(self.header_frame, text="[ LOGO ]", width=80, height=80, fg_color="gray30")
        self.label_logo.pack(side="left", padx=(0, 20))
        self.label_titulo = ctk.CTkLabel(self.header_frame, text="CONFIGURACIÓN DE LÍNEA", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(side="left")
        self.btn_volver = ctk.CTkButton(self.header_frame, text="Volver al Menú", width=100, fg_color="gray40", hover_color="gray30", command=self.volver_al_menu)
        self.btn_volver.pack(side="right")
        self.separador = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=(0, 20))
        self.label_instruccion = ctk.CTkLabel(self, text="Seleccione el formato de botella a inspeccionar:", font=("Roboto", 14), text_color="gray")
        self.label_instruccion.pack(pady=(10, 20))
        self.selector_formato = ctk.CTkOptionMenu(self, values=["Botella Tipo A", "Botella Tipo B", "Botella Tipo C", "Botella Tipo D", "Botella Tipo E"], width=250, height=40, font=("Roboto", 14))
        self.selector_formato.pack(pady=10)
        self.btn_arrancar = ctk.CTkButton(self, text="ARRANCAR INSPECCIÓN", width=250, height=50, font=("Roboto", 16, "bold"), fg_color="green", hover_color="darkgreen")
        self.btn_arrancar.pack(pady=30)
    def volver_al_menu(self):
        self.destroy()
        self.parent.deiconify()


# ==========================================
# 2. PANEL CENTRAL (DASHBOARD)
# ==========================================
class PantallaMenuPrincipal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Panel Central - Milcast Corp")
        self.geometry("650x550")
        self.resizable(False, False)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sistema)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=20, pady=20)

        ruta_script = os.path.dirname(__file__) 
        ruta_logo = os.path.join(ruta_script, "Aranjuez_logo.png")
        try:
            pil_image = Image.open(ruta_logo)
            self.ctk_logo = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(80, 80))
            self.label_logo = ctk.CTkLabel(self.header_frame, text="", image=self.ctk_logo)
        except:
            self.label_logo = ctk.CTkLabel(self.header_frame, text="[ LOGO ]", width=80, height=80, fg_color="gray30")
        self.label_logo.pack(side="left", padx=(0, 20))

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="MENÚ PRINCIPAL", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(side="left")

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=(20, 10))

        ancho_btn = 160
        alto_btn = 140
        fuente_btn = ("Roboto", 16, "bold")

        # --- AHORA ESTE BOTÓN ABRE LA PANTALLA DE USUARIOS ---
        self.btn_usuarios = ctk.CTkButton(self.grid_frame, text="👤\n\nUsuarios", width=ancho_btn, height=alto_btn, 
                                          font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.abrir_usuarios)
        self.btn_usuarios.grid(row=0, column=0, padx=15, pady=15)

        self.btn_botellas = ctk.CTkButton(self.grid_frame, text="🍾\n\nTipo de Botella", width=ancho_btn, height=alto_btn, 
                                          font=fuente_btn, fg_color="#1f538d", hover_color="#14375e", command=self.abrir_inspeccion)
        self.btn_botellas.grid(row=0, column=1, padx=15, pady=15)

        self.btn_bd = ctk.CTkButton(self.grid_frame, text="📊\n\nBase de Datos", width=ancho_btn, height=alto_btn, 
                                    font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.en_construccion)
        self.btn_bd.grid(row=1, column=0, padx=15, pady=15)

        self.btn_opcion1 = ctk.CTkButton(self.grid_frame, text="⚙️\n\nOpción 1", width=ancho_btn, height=alto_btn, 
                                         font=fuente_btn, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.en_construccion)
        self.btn_opcion1.grid(row=1, column=1, padx=15, pady=15)

    def abrir_usuarios(self):
        self.withdraw()
        ventana_usuarios = PantallaUsuarios(self)
        ventana_usuarios.focus()

    def abrir_inspeccion(self):
        self.withdraw()
        ventana_inspeccion = PantallaInspeccion(self)
        ventana_inspeccion.focus()

    def en_construccion(self):
        print("Este módulo aún está en desarrollo.")

    def cerrar_sistema(self):
        self.parent.destroy()


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
        usuario_ingresado = self.entry_usuario.get().strip()
        password_ingresada = self.entry_password.get().strip()

        # --- AHORA LEEMOS LOS USUARIOS REALES DESDE EL JSON ---
        usuarios_db = cargar_usuarios()

        # Verificamos si el usuario existe y si la contraseña coincide
        if usuario_ingresado in usuarios_db and usuarios_db[usuario_ingresado] == password_ingresada:
            self.withdraw() 
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