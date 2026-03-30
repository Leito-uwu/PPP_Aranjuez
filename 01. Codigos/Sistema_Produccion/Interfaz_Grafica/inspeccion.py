import customtkinter as ctk
import os
from PIL import Image

class PantallaInspeccion(ctk.CTkToplevel):
    # 🟢 AÑADIMOS formato_actual y on_cambio_formato
    def __init__(self, on_volver, formato_actual, on_cambio_formato):
        super().__init__()
        self.on_volver = on_volver 
        self.on_cambio_formato = on_cambio_formato # El cable hacia main.py
        
        self.title("Configuración de Botellas - Milcast Corp")
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

        self.label_titulo = ctk.CTkLabel(self.header_frame, text="CONFIGURACIÓN DE LÍNEA", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(side="left")

        self.btn_volver = ctk.CTkButton(self.header_frame, text="Volver al Menú", width=100, 
                                        fg_color="gray40", hover_color="gray30", command=self.cerrar_ventana)
        self.btn_volver.pack(side="right")

        self.separador = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=(0, 20))

        # --- CUERPO ---
        self.label_instruccion = ctk.CTkLabel(self, text="Seleccione el formato a inspeccionar:", font=("Roboto", 14), text_color="gray")
        self.label_instruccion.pack(pady=(10, 20))

        opciones_botellas = ["Botella Tipo A", "Botella Tipo B", "Botella Tipo C", "Botella Tipo D", "Botella Tipo E"]
        self.selector_formato = ctk.CTkOptionMenu(self, values=opciones_botellas, command=self.al_cambiar_formato, width=250, height=40, font=("Roboto", 14))
        self.selector_formato.pack(pady=10)
        
        # 🟢 HACEMOS QUE EL SELECTOR EMPIECE EN EL FORMATO GUARDADO
        self.selector_formato.set(formato_actual)

        self.label_estado = ctk.CTkLabel(self, text=f"Formato actual: {formato_actual}", font=("Roboto", 16), text_color="yellow")
        self.label_estado.pack(pady=20)

        self.btn_arrancar = ctk.CTkButton(self, text="ARRANCAR INSPECCIÓN", width=250, height=50, font=("Roboto", 16, "bold"), fg_color="green", hover_color="darkgreen")
        self.btn_arrancar.pack(pady=30)

    def al_cambiar_formato(self, eleccion):
        self.label_estado.configure(text=f"Formato actual: {eleccion}")
        # 🟢 LE AVISAMOS AL MAIN.PY QUE CAMBIAMOS DE BOTELLA
        self.on_cambio_formato(eleccion)

    def cerrar_ventana(self):
        self.destroy()
        self.on_volver()