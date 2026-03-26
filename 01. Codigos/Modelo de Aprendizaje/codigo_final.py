import cv2
import numpy as np
import tensorflow as tf

# Importamos tus módulos de preprocesamiento
from Preprocesamiento.Centrado import trabajar_con_contorno_blanco
from Preprocesamiento.Cortado import recortar_botella_dinamico
from Preprocesamiento.Filtrado import procesar_imagen

# 1. CARGAMOS EL MODELO UNA SOLA VEZ AL ENCENDER EL PROGRAMA
print("Iniciando sistema... Cargando el cerebro .keras...")
modelo_inspector = tf.keras.models.load_model(r"C:\Users\leona\Documents\PPP_Aranjuez\01. Codigos\Modelo de Aprendizaje\modelo_inspector_botellas.keras")
print("✅ Sistema listo.\n")

def inspeccionar_botella(ruta_foto_camara):
    """
    Recibe la ruta de la foto cruda de la cámara, hace todo en memoria RAM
    y devuelve directamente el string 'BUENA' o 'MALA'.
    """
    # 1. La cámara entrega la foto cruda
    imagen_cruda = cv2.imread(ruta_foto_camara, cv2.IMREAD_GRAYSCALE)
    if imagen_cruda is None:
        return "ERROR: No se pudo leer la foto"

    # ====================================================
    # TODO ESTO OCURRE EN LA MEMORIA RAM (NO SE GUARDA NADA)
    # ====================================================
    # 2. Preprocesamiento
    bbox = trabajar_con_contorno_blanco(imagen_cruda)
    if bbox is None:
        return "ERROR: No se detectó ninguna botella en la foto"
        
    img_recortada = recortar_botella_dinamico(imagen_cruda, bbox)
    img_procesada = procesar_imagen(img_recortada) # Sale 224x224 en grises

    # 3. Adaptar la matriz para Keras (De 1 canal a 3 canales)
    img_3_canales = np.stack((img_procesada,)*3, axis=-1)
    img_para_ia = np.expand_dims(img_3_canales, axis=0)

    # 4. La IA evalúa la matriz directamente
    prediccion = modelo_inspector.predict(img_para_ia, verbose=0)
    
    # ====================================================
    # VEREDICTO FINAL
    # ====================================================
    es_mala = prediccion[0][0] > 0.5
    
    if es_mala:
        return "MALA"
    else:
        return "BUENA"

# ==========================================
# SIMULACIÓN DE 1 DISPARO DE LA CÁMARA
# ==========================================
if __name__ == "__main__":
    # Simula que la cámara acaba de tomar esta foto y te la mandó
    foto_cruda = r"C:\Users\leona\Documents\PPP_Aranjuez\01. Codigos\Imagenes_Pruebas\Botellas_Buenas\B_B0001.JPG" # Ajusta al nombre de tu foto
    
    # Ejecutamos la función
    resultado = inspeccionar_botella(foto_cruda)
    
    # Imprimimos la decisión final que mandarías al autómata
    print(f"La botella inspeccionada es: {resultado}")