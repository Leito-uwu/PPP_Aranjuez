# Importamos las librerías necesarias y nuestros módulos
import os
from tensorflow.keras.callbacks import EarlyStopping
from Datos import cargar_datasets
from Arquitectura import construir_modelo_inspector

def entrenar_y_guardar(ruta_dataset, ruta_guardado_keras, epocas=15):

    train_ds, val_ds = cargar_datasets(ruta_dataset)
    modelo = construir_modelo_inspector()
    parada_temprana = EarlyStopping(
        monitor='val_accuracy', 
        patience=3, 
        restore_best_weights=True
    )
    #  Comienza a Entrenar
    historial = modelo.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epocas,
        callbacks=[parada_temprana]
    )
    
    
    # Guardar el modelo
    modelo.save(ruta_guardado_keras)

if __name__ == "__main__":
    # Se debe cambiar las rutas del Google Drive
    RUTA_DATASET = '/content/drive/MyDrive/PPP/Dataset_Final/'
    RUTA_GUARDADO = '/content/drive/MyDrive/PPP/modelo_inspector_botellas.keras'
    
    entrenar_y_guardar(RUTA_DATASET, RUTA_GUARDADO)