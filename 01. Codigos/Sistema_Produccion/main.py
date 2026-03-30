import customtkinter as ctk
from Interfaz_Grafica.login import PantallaLogin
from Interfaz_Grafica.dashboard import PantallaMenuPrincipal 
from Interfaz_Grafica.inspeccion import PantallaInspeccion
from Interfaz_Grafica.gestor_usuarios import PantallaUsuarios
from Interfaz_Grafica.pantalla_bd import PantallaBaseDatos 

class AplicacionPrincipal:
    def __init__(self):
        # 🟢 ESTADO GLOBAL: Memoria central de la máquina
        self.formato_actual = "Botella Tipo A" 
        
        self.mostrar_login()

    def mostrar_login(self):
        self.login_vnt = PantallaLogin(on_login_success=self.abrir_menu_principal)
        self.login_vnt.mainloop()

    def abrir_menu_principal(self):
        self.menu_vnt = PantallaMenuPrincipal(
            on_abrir_botellas=self.abrir_inspeccion,
            on_abrir_usuarios=self.abrir_usuarios,
            on_abrir_bd=self.abrir_base_datos
        )

    # --- CONTROLADORES DE VENTANAS SECUNDARIAS ---
    def abrir_inspeccion(self):
        self.menu_vnt.withdraw()
        # Le enviamos el formato actual y el "cable" para actualizarlo
        self.ventana_inspeccion = PantallaInspeccion(
            on_volver=self.mostrar_menu,
            formato_actual=self.formato_actual,
            on_cambio_formato=self.actualizar_formato
        ) 
        self.ventana_inspeccion.focus()

    # 🟢 FUNCIÓN QUE RECIBE EL CAMBIO DE BOTELLA
    def actualizar_formato(self, nuevo_formato):
        self.formato_actual = nuevo_formato
        print(f"🔄 Sistema central actualizado a: {self.formato_actual}")

    def abrir_usuarios(self):
        self.menu_vnt.withdraw()
        self.ventana_usuarios = PantallaUsuarios(on_volver=self.mostrar_menu)
        self.ventana_usuarios.focus()
    
    def abrir_base_datos(self):
        self.menu_vnt.withdraw()
        # Le enviamos el formato actual a la pantalla de BD
        self.ventana_bd = PantallaBaseDatos(
            on_volver=self.mostrar_menu,
            formato_actual=self.formato_actual
        )
        self.ventana_bd.focus()

    def mostrar_menu(self):
        self.menu_vnt.deiconify()

if __name__ == "__main__":
    app = AplicacionPrincipal()