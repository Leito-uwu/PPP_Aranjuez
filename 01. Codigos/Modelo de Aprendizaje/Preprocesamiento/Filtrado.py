import cv2

def procesar_imagen(imagen_recortada,tamano_final = (224,224)):
    if imagen_recortada is None:
        return None
    
    imagen_procesada = imagen_recortada
    # Filtro Gausseano
    # Un kernel de (5,5) 
    imagen_procesada = cv2.GaussianBlur(imagen_procesada,(5,5),0)

    # Redimensionamiento de la Imagen
    imagen_final = cv2.resize(imagen_procesada, tamano_final, interpolation=cv2.INTER_AREA)
    
    return imagen_final
