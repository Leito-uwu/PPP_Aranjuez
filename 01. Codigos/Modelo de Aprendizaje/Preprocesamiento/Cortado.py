import cv2

def recortar_botella_dinamico(imagen_original, bbox, margen=20):
 
    if bbox is None:
        return None
        
    x, y, w, h = bbox
    alto_img, ancho_img = imagen_original.shape[:2]

    # Calcular las coordenadas con margen
    # max() y min() aseguran que si el margen no se salga del limite
    x_inicio = max(0, x - margen)
    y_inicio = max(0, y - margen)
    
    x_fin = min(ancho_img, x + w + margen)
    y_fin = min(alto_img, y + h + margen)
    
    # Recortar
    recorte = imagen_original[y_inicio:y_fin, x_inicio:x_fin]
    
    return recorte
    
    