import customtkinter as ctk
# Importamos las funciones de la base de datos (suponiendo que están en Base_Datos/gestor_usuarios.py)
# Por ahora, si no has movido eso, usamos una validación simple o la importación correcta
from Base_Datos.gestor_usuarios import cargar_usuarios

class PantallaLogin(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success # Función que llamaremos al tener éxito
        
        self.title("Milcast Corp - Acceso")
        self.geometry("400x450")
        self.resizable(False, False) 
        
        # --- UI ---
        self.label_titulo = ctk.CTkLabel(self, text="SISTEMA DE INSPECCIÓN", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(pady=(50, 5))
        
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="ID de Operador", width=250, height=40, justify="center")
        self.entry_usuario.pack(pady=10)
        
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250, height=40, justify="center")
        self.entry_password.pack(pady=10)
        
        self.label_mensaje = ctk.CTkLabel(self, text="", font=("Roboto", 12))
        self.label_mensaje.pack(pady=5)
        
        self.btn_ingresar = ctk.CTkButton(self, text="INICIAR SESIÓN", width=250, height=40, 
                                          font=("Roboto", 14, "bold"), command=self.validar_acceso)
        self.btn_ingresar.pack(pady=20)
        
    def validar_acceso(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        usuarios_db = cargar_usuarios() # Leemos del JSON

        # En tu login.py, busca esta parte y déjala así:
        if usuario in usuarios_db and usuarios_db[usuario] == password:
            self.withdraw() # <--- ¡CAMBIA DESTROY POR WITHDRAW!
            self.on_login_success()
        else:
            self.label_mensaje.configure(text="❌ Credenciales incorrectas", text_color="red")