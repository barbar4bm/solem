import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import base64 as b64
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

def b64_openCV(imgenb64):
  im_bytes = b64.b64decode(imgenb64)
  im_arr = np.frombuffer(im_bytes, dtype=np.uint8) 
  img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR) 
  return img 

def openCV_b64(imagenOpenCV):
    # Codificar la imagen en formato JPEG
    _, buffer = cv2.imencode('.jpg', imagenOpenCV)
    
    # Convertir la imagen codificada en un string base64
    imagen_base64 = b64.b64encode(buffer).decode('utf-8')

    return imagen_base64

def imagen_a_matriz(imagen_data):
    # Si los datos ya son en formato bytes
    if isinstance(imagen_data, bytes):
        imagen_bytes = np.frombuffer(imagen_data, dtype=np.uint8)
    else:
        imagen_bytes = np.asarray(bytearray(imagen_data), dtype=np.uint8)
    
    imagen = cv2.imdecode(imagen_bytes, cv2.IMREAD_COLOR)
    return imagen

def escalaGrises(imagen):
    return cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)

def leerQR(image):

    # Inicializar el detector de códigos QR con OpenCV
    qr_code_detector = cv2.QRCodeDetector()

    # Si no es un arreglo de numpy, lanzar una excepción
    if not isinstance(image, np.ndarray):
        raise ValueError("El argumento 'image' debe ser un arreglo de numpy (imagen de OpenCV).")
    
    # Detectar y decodificar el código QR
    value, pts, qr_code = qr_code_detector.detectAndDecode(image)
    return value
    

def leer_base64_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido

def guardar_base64_en_archivo(img, nombre_archivo):
    """Guarda la representación base64 de una imagen de OpenCV en un archivo. 
    Si hay un error, se devuelve False. Si tiene éxito, devuelve True."""
    try:
        img_base64 = openCV_b64(img)
        
        with open(nombre_archivo, 'w') as f:
            f.write(img_base64)
        
        return True
    except Exception as e:
        print(f"Ocurrió un error al guardar la imagen en base64: {e}")
        return False
    
def cargar_imagenes(nombres, formato, ruta):
    """
    Carga una lista de imágenes a partir de sus nombres, formato y ruta.
    
    Parámetros:
    - nombres (list): Lista de nombres de archivos sin extensión.
    - formato (str): Formato de los archivos, ej: '.png', '.jpg'.
    - ruta (str): Ruta del directorio donde se encuentran las imágenes.

    Retorna:
    - list: Lista de imágenes cargadas.
    """
    # Crear lista completa de rutas a las imágenes
    rutas_completas = [os.path.join(ruta, nombre + formato) for nombre in nombres]

    # Leer las imágenes y almacenarlas en la lista
    imagenes = [cv2.imread(ruta_completa) for ruta_completa in rutas_completas]

    return imagenes

def numpy_to_png(imagen_np):
    """Convierte una matriz numpy a bytes de imagen PNG."""
    retval, buffer_png = cv2.imencode('.png', imagen_np)
    png_bytes = buffer_png.tobytes()
    return png_bytes

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


def escalar_imagen(img, altura, anchura):
    
    if not isinstance(img, np.ndarray):
        raise ValueError("El parámetro 'img' debe ser un objeto numpy.ndarray.")
    
    return cv2.resize(img, (anchura, altura))

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