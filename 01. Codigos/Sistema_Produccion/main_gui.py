import customtkinter as CTk
root  = CTk.CTk()
button = CTk.CTkButton(root,text = "Hola mundo")
button.pack()
root.mainloop()

## Para personalizar los Widgets
button.config(background = "red")   # Para cambiar el color del boton
button.configure(width = 100, heigth = 50) # Ver el tamano del boton
#button.shape("circle") # Cambiar la figura del boton
