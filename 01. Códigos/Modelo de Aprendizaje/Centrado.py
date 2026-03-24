# CELDA: Módulo Detector - Aislando el Contorno Blanco
import cv2
import numpy as np
import matplotlib.pyplot as plt

def trabajar_con_contorno_blanco(imagen_bgr_original, debug=False):
    """
    Binariza la imagen y separa la botella de la máquina usando morfología
    para extraer únicamente el Bounding Box de la botella cruda.
    """
    alto_orig, ancho_orig = imagen_bgr_original.shape[:2]

    escala = 800.0 / ancho_orig
    nuevo_ancho = 800
    nuevo_alto = int(alto_orig * escala)
    imagen_trabajo = cv2.resize(imagen_bgr_original, (nuevo_ancho, nuevo_alto))
    centro_foto_x = nuevo_ancho // 2
    centro_foto_y = nuevo_alto // 2

    # 1. Filtros (Los que ya demostraron funcionar en tu imagen)
    gris = cv2.cvtColor(imagen_trabajo, cv2.COLOR_BGR2GRAY)
    gris_suavizado = cv2.medianBlur(gris, 15)

    # 2. Binarización Adaptativa (Convierte el cuello negro a blanco)
    binarizada = cv2.adaptiveThreshold(gris_suavizado, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 201, 10)

    # ---------------------------------------------------------
    # 3. NUEVO PASO CLAVE: DESCONECTAR LA MÁQUINA DE LA BOTELLA
    # Usamos un kernel (pincel) elíptico grande para romper las uniones.
    # Si la máquina sigue pegada, aumenta este número (ej. a 25, 25).
    # ---------------------------------------------------------
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    binarizada_limpia = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel)

    # 4. Encontrar contornos en la imagen ya limpia y separada
    contornos, _ = cv2.findContours(binarizada_limpia, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mejor_contorno = None
    mejor_distancia = float('inf')

    for c in contornos:
        area = cv2.contourArea(c)
        if area < 10000: continue # Ignorar basura pequeña

        M = cv2.moments(c)
        if M["m00"] == 0: continue

        cx_contorno = int(M["m10"] / M["m00"])
        cy_contorno = int(M["m01"] / M["m00"])

        distancia_al_centro = np.sqrt((cx_contorno - centro_foto_x)**2 + (cy_contorno - centro_foto_y)**2)

        # Nos quedamos con la forma blanca más cercana al centro de la foto
        if distancia_al_centro < mejor_distancia:
            mejor_distancia = distancia_al_centro
            mejor_contorno = c

    if mejor_contorno is not None:
        # Extraer Bounding Box y re-escalar al tamaño original
        x, y, w, h = cv2.boundingRect(mejor_contorno)
        bbox_orig = (int(x/escala), int(y/escala), int(w/escala), int(h/escala))

        if debug:
            plt.figure(figsize=(20, 5))
            plt.subplot(1, 4, 1); plt.imshow(gris_suavizado, cmap='gray'); plt.title("1. Blur")
            plt.subplot(1, 4, 2); plt.imshow(binarizada, cmap='gray'); plt.title("2. Binarizado (PEGADO)")
            plt.subplot(1, 4, 3); plt.imshow(binarizada_limpia, cmap='gray'); plt.title("3. Limpio (SEPARADO)")

            # Dibujar el contorno ganador sobre la limpia para verificar
            img_verificacion = cv2.cvtColor(binarizada_limpia, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(img_verificacion, [mejor_contorno], -1, (0, 255, 0), 5)
            plt.subplot(1, 4, 4); plt.imshow(img_verificacion); plt.title("4. Contorno Elegido")
            plt.show()

        return bbox_orig
    else:
        return None