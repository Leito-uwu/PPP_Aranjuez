# CELDA: Módulo Recortador
import cv2
import numpy as np

def recortar_botella_dinamico(imagen_bgr_original, bbox, margen=20):
    """
    Recorta la región de interés (ROI) de la botella usando su Bounding Box.
    Añade un margen de seguridad (padding) para no perder bordes en la IA.
    Protege contra recortes fuera de los límites de la imagen.
    """
    if bbox is None:
        return None
        
    x, y, w, h = bbox
    alto_img, ancho_img = imagen_bgr_original.shape[:2]

    # 1. Calcular las coordenadas con margen
    # max() y min() aseguran que si el margen se sale de la foto, se detenga en el borde (0 o el límite)
    x_inicio = max(0, x - margen)
    y_inicio = max(0, y - margen)
    
    x_fin = min(ancho_img, x + w + margen)
    y_fin = min(alto_img, y + h + margen)
    
    # 2. Realizar el recorte (Slicing de arrays en NumPy)
    recorte = imagen_bgr_original[y_inicio:y_fin, x_inicio:x_fin]
    
    return recorte
    
    