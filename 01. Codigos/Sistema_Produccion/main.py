import customtkinter as ctk
from Interfaz_Grafica.login import PantallaLogin
from Interfaz_Grafica.dashboard import PantallaMenuPrincipal 
from Interfaz_Grafica.inspeccion import PantallaInspeccion
from Interfaz_Grafica.gestor_usuarios import PantallaUsuarios
from Interfaz_Grafica.pantalla_bd import PantallaBaseDatos # 1. IMPORTAMOS LA PANTALLA SCADA

class AplicacionPrincipal:
    def __init__(self):
        self.mostrar_login()

    def mostrar_login(self):
        self.login_vnt = PantallaLogin(on_login_success=self.abrir_menu_principal)
        self.login_vnt.mainloop() # Este es el ÚNICO mainloop que necesita el programa

    def abrir_menu_principal(self):
        print("🚀 Login exitoso. Iniciando Dashboard...")
        # Instanciamos el menú y le conectamos todas las rutas
        self.menu_vnt = PantallaMenuPrincipal(
            on_abrir_botellas=self.abrir_inspeccion,
            on_abrir_usuarios=self.abrir_usuarios,
            on_abrir_bd=self.abrir_base_datos # 2. CONECTAMOS EL BOTÓN
        )

    # --- CONTROLADORES DE VENTANAS SECUNDARIAS ---
    def abrir_inspeccion(self):
        self.menu_vnt.withdraw()
        self.ventana_inspeccion = PantallaInspeccion(on_volver=self.mostrar_menu) 
        self.ventana_inspeccion.focus()

    def abrir_usuarios(self):
        self.menu_vnt.withdraw()
        self.ventana_usuarios = PantallaUsuarios(on_volver=self.mostrar_menu)
        self.ventana_usuarios.focus()

    def abrir_base_datos(self): # 3. LA FUNCIÓN QUE ABRE LA BD
        self.menu_vnt.withdraw()
        self.ventana_bd = PantallaBaseDatos(on_volver=self.mostrar_menu)
        self.ventana_bd.focus()

    def mostrar_menu(self):
        self.menu_vnt.deiconify()

if __name__ == "__main__":
    app = AplicacionPrincipal()