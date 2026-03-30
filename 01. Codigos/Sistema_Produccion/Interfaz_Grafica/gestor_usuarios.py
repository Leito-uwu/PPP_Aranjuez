import customtkinter as ctk
import os
from PIL import Image
from Base_Datos.gestor_usuarios import cargar_usuarios, guardar_usuarios

class PantallaUsuarios(ctk.CTkToplevel):
    def __init__(self, on_volver):
        super().__init__()
        self.on_volver = on_volver
        
        self.title("Gestión de Usuarios - Milcast Corp")
        self.geometry("650x500")
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

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="GESTIÓN DE USUARIOS", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(side="left")

        self.btn_volver = ctk.CTkButton(self.header_frame, text="Volver al Menú", width=100, 
                                        fg_color="gray40", hover_color="gray30", command=self.cerrar_ventana)
        self.btn_volver.pack(side="right")

        self.separador = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=(0, 10))

        # --- CUERPO DIVIDIDO ---
        self.frame_izq = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_izq.pack(side="left", fill="both", expand=True, padx=20)
        
        self.frame_der = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_der.pack(side="right", fill="both", expand=True, padx=20)

        # CREAR USUARIO
        self.lbl_crear = ctk.CTkLabel(self.frame_izq, text="➕ Crear Nuevo Operador", font=("Roboto", 16, "bold"), text_color="#4CAF50")
        self.lbl_crear.pack(pady=10)
        self.entry_nuevo_id = ctk.CTkEntry(self.frame_izq, placeholder_text="Nuevo ID de Operador", width=200)
        self.entry_nuevo_id.pack(pady=10)
        self.entry_nueva_pass = ctk.CTkEntry(self.frame_izq, placeholder_text="Contraseña", width=200)
        self.entry_nueva_pass.pack(pady=10)
        self.btn_crear = ctk.CTkButton(self.frame_izq, text="Guardar Usuario", fg_color="green", hover_color="darkgreen", command=self.crear_usuario)
        self.btn_crear.pack(pady=15)

        # ELIMINAR USUARIO
        self.lbl_eliminar = ctk.CTkLabel(self.frame_der, text="🗑️ Eliminar Operador", font=("Roboto", 16, "bold"), text_color="#F44336")
        self.lbl_eliminar.pack(pady=10)
        self.lbl_instruccion = ctk.CTkLabel(self.frame_der, text="Seleccione el ID a eliminar:", font=("Roboto", 12))
        self.lbl_instruccion.pack(pady=(10, 0))
        self.selector_eliminar = ctk.CTkOptionMenu(self.frame_der, values=["Cargando..."], width=200)
        self.selector_eliminar.pack(pady=10)
        self.btn_eliminar = ctk.CTkButton(self.frame_der, text="Eliminar Usuario", fg_color="#d32f2f", hover_color="#9a0007", command=self.eliminar_usuario)
        self.btn_eliminar.pack(pady=15)

        self.lbl_mensaje = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.lbl_mensaje.pack(side="bottom", pady=20)

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

    def cerrar_ventana(self):
        self.destroy()
        self.on_volver()