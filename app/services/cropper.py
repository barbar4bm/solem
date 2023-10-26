import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os

def obtenerRecorteImagen(imagenbaseEq,imgEq,M):
  # Definimos las dimensiones del rectángulo base (el original de la imagen de referencia)
  h,w = imagenbaseEq.shape
  pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
  # Desenvolvemos la imagen utilizando la homografía inversa
  warped = cv2.warpPerspective(imgEq, np.linalg.inv(M), (w, h))
  if warped.dtype != np.uint8:
    warped = (warped * 255).astype(np.uint8)
  return warped

def recorte(rut_bin, rut_bin2):
    
    # 500x800
    rut_bin=escalar_imagen(rut_bin,530,840)
    rut_bin2=escalar_imagen(rut_bin2,530,840)

    #anverso
    nombres = rut_bin[171:211 , 291:806]
    apellidos = rut_bin[88:152 , 292:520]
    RUN = rut_bin[460:496 , 98:273]
    nacionalidad = rut_bin[220:265, 291:425]
    sexo = rut_bin[222:263, 450:600]
    fecha_nacimiento = rut_bin[276:311 , 250:480]
    numero_documento = rut_bin[275:310, 487:663]
    fecha_emision = rut_bin[330:369 , 292:463]
    fecha_vencimiento = rut_bin[335:367 , 477:667]

    #reverso
    ciudad = rut_bin2[211:247 , 182:600]
    profesion = rut_bin2[242:274,182:403]
    mrz = rut_bin2[354:492, 42:800]
    nombre_mrz = rut_bin2[440:482, 418:800]
    apellido_mrz = rut_bin2[440:478, 44:375]
    rut_mrz = rut_bin2[395:440,495:747]
    documento_mrz = rut_bin2[354:398,170:400]
    qr=recortar_qr(rut_bin2)

    return {
        "nombres": nombres,
        "apellidos": apellidos,
        "RUN": RUN,
        "nacionalidad": nacionalidad,
        "sexo": sexo,
        "fecha_nacimiento": fecha_nacimiento,
        "numero_documento": numero_documento,
        "fecha_emision": fecha_emision,
        "fecha_vencimiento": fecha_vencimiento,
        "ciudad": ciudad,
        "profesion": profesion,
        "mrz": mrz,
        "nombre_mrz": nombre_mrz,
        "apellido_mrz": apellido_mrz,
        "rut_mrz": rut_mrz,
        "documento_mrz": documento_mrz,
        "qr":qr
    }

def guardar_recortes(diccionario):
    """
    Toma un diccionario donde cada clave-valor corresponde a un nombre y una imagen, respectivamente.
    Guarda cada imagen en una carpeta llamada "recortes" con un nombre correspondiente a su clave en formato PNG.
    
    Parámetros:
    - diccionario (dict): Diccionario de imágenes.
    """
    
    # Crear la carpeta "recortes" si no existe
    if not os.path.exists('recortes'):
        os.makedirs('recortes')
        
    for clave, imagen in diccionario.items():
        ruta = os.path.join('recortes', f'{clave}.png')
        cv2.imwrite(ruta, imagen)

def recortar_qr(imagen):
    # Coordenadas del rectángulo donde se encuentra el QR
    x = 23
    y = 30
    w = 170
    h = 170

    # Recortar la imagen
    qr_recortado = imagen[y:y+h, x:x+w]
    return qr_recortado    

def escalar_imagen(img, altura, anchura):
    
    if not isinstance(img, np.ndarray):
        raise ValueError("El parámetro 'img' debe ser un objeto numpy.ndarray.")
    
    return cv2.resize(img, (anchura, altura))

