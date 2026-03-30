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

import time

import time
import os
import glob

# ==========================================
# SIMULACIÓN CONTINUA DE LA LÍNEA DE PRODUCCIÓN
# ==========================================
if __name__ == "__main__":
    # 1. Ahora apuntamos a la CARPETA, no a una sola foto
    carpeta_pruebas = r"C:\Users\leona\Documents\PPP_Aranjuez\01. Codigos\Imagenes_Pruebas\Botellas_Malas"
    
    # 2. Buscamos todas las imágenes JPG en esa carpeta
    patron_busqueda = os.path.join(carpeta_pruebas, "*.JPG")
    lista_fotos = glob.glob(patron_busqueda)
    
    # También buscamos en minúsculas por si acaso (.jpg)
    lista_fotos.extend(glob.glob(os.path.join(carpeta_pruebas, "*.jpg")))

    if len(lista_fotos) == 0:
        print("⚠️ No se encontraron imágenes en la carpeta seleccionada.")
    else:
        print(f"📦 Lote detectado: {len(lista_fotos)} botellas en la línea.\n")
        
        # 3. Iniciamos el ciclo de la cinta transportadora
        for indice, ruta_foto in enumerate(lista_fotos, start=1):
            nombre_archivo = os.path.basename(ruta_foto)
            print(f"📸 [Botella {indice}/{len(lista_fotos)}] Inspeccionando: {nombre_archivo}...")
            
            # --- INICIO DEL CRONÓMETRO ---
            inicio_timer = time.time()
            
            resultado = inspeccionar_botella(ruta_foto)
            
            # --- FIN DEL CRONÓMETRO ---
            tiempo_ciclo_ms = (time.time() - inicio_timer) * 1000
            
            print("=========================================")
            print(f"Veredicto: {resultado}")
            print(f"Tiempo: {tiempo_ciclo_ms:.2f} ms")
            print("=========================================")
            
            # 4. PAUSA DEL SISTEMA
            # El programa se congela aquí hasta que presiones Enter en la consola
            if indice < len(lista_fotos):
                input("👉 Presiona ENTER para procesar la siguiente botella (o Ctrl+C para salir)... \n")
        
        print("✅ Lote terminado. Cinta transportadora detenida.")