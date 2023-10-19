import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import base64 as b64
from pyzbar.pyzbar import decode
import os

def puntos_descriptores(image):
  sift = cv2.xfeatures2d.SIFT_create(0, 3, 0.04, 0, 2)
  puntos,descriptores=sift.detectAndCompute(image,None)
  return puntos,descriptores

def preparacionInicial(imagenInicial):
  #de BGR a RGB
  imagenInicialRGB = cv2.cvtColor(imagenInicial, cv2.COLOR_BGR2RGB)
  # Cambio de espacio de color BGR a GRAY
  gray = cv2.cvtColor(imagenInicialRGB, cv2.COLOR_BGR2GRAY)
  # Ecualización "Contrast Limited Adaptive Histogram Equalization,
  clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
  eq=clahe.apply(gray)

  return eq

def binarizacion(imagen, otsu=0):
    # Verificamos si otsu tiene valores válidos
    if otsu not in [0, 1]:raise ValueError("El valor de otsu debe ser 0 o 1.")

    if otsu == 1:
       return cv2.threshold(imagen, 127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
       
    else:
       return cv2.threshold(imagen,127,255,cv2.THRESH_BINARY)

def findMatches(descriptoresObjeto,descriptoresBase):
  """Idealmente tener una base de datos de entrenamiento de los descripores base,
     para luego simplemente consultar estos datos y buscar coincidencias,"""   
   
  FLANN_INDEX_KDTREE = 1
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)

  matches = flann.knnMatch(descriptoresObjeto,descriptoresBase,k=2)
  good = []
  for m,n in matches:
    if m.distance < 0.7*n.distance:
      good.append(m)
  
  return good
    
def calcHomografia(good,MIN_MATCH_COUNT,img_ref,kp_obj,kp_ref,imgEq):
    """Como se puede consultar a los datos de entrenamiento
    y no enviar la imagen_base como parametro?"""
  #Homografia
    if len(good)>MIN_MATCH_COUNT:
      #la coincidencia m posee el indice que hace referencia al keypoint de la lista kp_obj
        src_pts = np.float32([ kp_obj[m.queryIdx].pt for m in good ]).reshape(-1,1,2) # para cada coincidencia m, se accede al atributo .queryIdx (indice del descriptor)

        dst_pts = np.float32([ kp_ref[m.trainIdx].pt for m in good ]).reshape(-1,1,2) #
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        h,w = img_ref.shape
        #pts: puntos que forman un rectangulo en base a las medidas de img2
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

        #tomar el conjunto de puntos (pts) de img2 y aplicar la trasnformacion de perspectiva de puntos con la MAtriz de homografia M
        #dst contiene conjuntos de puntos que encuadran el carnet
        dst = cv2.perspectiveTransform(pts,M)

        return dst, M, matchesMask
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None
        return None
    
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


def leerQR(imagen):
    # Usa pyzbar para decodificar el código QR
    codigos_qr = decode(imagen)
    
    # Si encontramos algún código QR, devolvemos su contenido
    for qr in codigos_qr:
        return qr.data.decode('utf-8')
    
    # Si no se encuentra ningún código QR, devolvemos None
    return None
    

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