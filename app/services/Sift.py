import pickle as pkl
import copyreg
import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import glob
from services import tools


def _pickle_keypoints(point):
    return cv2.KeyPoint, (point.pt[0], point.pt[1], point.size, point.angle,
                          point.response, point.octave, point.class_id)

# Registramos la función de ayuda para serializar objetos cv2.KeyPoint
copyreg.pickle(cv2.KeyPoint().__class__, _pickle_keypoints)

def retornoPrueba():
    return 'return prueba'

def almacenar_descriptores():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_names = ["anverso", "reverso"]

    for name in image_names:
        found_images = glob.glob(os.path.join(BASE_DIR, 'data', f'{name}.*'))
        if not found_images:
            print(f"Imagen {name} no encontrada.")
            continue

        IMAGE_PATH = found_images[0]
        image = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"La imagen {IMAGE_PATH} no se cargó correctamente.")

        sift = cv2.SIFT_create()
        kp, descriptores = sift.detectAndCompute(image, None)

        # Almacenar keypoints
        # Convertir los keypoints a una estructura serializable
        SAVE_PATH = os.path.join(BASE_DIR, 'data', f'keypoints_{name}.pkl')

        try:
            guardar_keypoints(kp, name)
        except Exception as e:
            print(f"Error al guardar keypoints: {e}")


        dic = {name: descriptores}
        SAVE_PATH = os.path.join(BASE_DIR, 'data', f'descriptores_{name}.pkl')
        try:
            with open(SAVE_PATH, 'wb') as f:
                pkl.dump(dic, f)
        except Exception as e:
            print(f"Error al guardar descriptores: {e}")

    return True

def preparacionInicial(imagenInicial,lado,claves_omitidas=None, tipo_procesamiento='procesar_imagen'):
    if isinstance(imagenInicial, dict):
        # Si claves_omitidas está vacío, se procesan todas las imágenes sin comprobar
        if not claves_omitidas:
            for clave, imagen in imagenInicial.items():
                imagenInicial[clave] = procesar_tipo(imagen,lado, tipo_procesamiento)
        else:
            # Si claves_omitidas no está vacío, se realiza la comprobación
            for clave, imagen in imagenInicial.items():
                if clave not in claves_omitidas and imagen is not None:
                    imagenInicial[clave] = procesar_tipo(imagen, lado, tipo_procesamiento)
                elif clave == 'qr':
                    imagenInicial[clave] = imagen
    else:
        imagenInicial = procesar_tipo(imagenInicial,lado,tipo_procesamiento)

    return imagenInicial

def procesar_tipo(imagen,lado, tipo_procesamiento):
    if tipo_procesamiento == 'procesar_imagen':
        #return bin_INV_OTSU(imagen)
        return procesar_imagen(imagen,lado)
    elif tipo_procesamiento == 'bin_INV_OTSU':
        return bin_INV_OTSU(imagen)
    elif tipo_procesamiento == 'bin_OTSU':
        return binarizacion(procesar_imagen(imagen,lado), 1)[1]
    elif tipo_procesamiento == 'bin':
        return binarizacion(imagen, 0)[1]
    else:
        return imagen  

def procesar_imagen(imagen,tipo=''):
    clipLimit=2.0
    if(tipo=='anverso'):
        clipLimit=0.8
    elif(tipo=='reverso'):
        clipLimit=1.5
    # de BGR a RGB
    imagenRGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    # Cambio de espacio de color BGR a GRAY
    gray = cv2.cvtColor(imagenRGB, cv2.COLOR_BGR2GRAY)
    # Ecualización "Contrast Limited Adaptive Histogram Equalization,
    clahe = cv2.createCLAHE(clipLimit, tileGridSize=(8,8))
    eq = clahe.apply(gray)
    return eq

def bin_INV_OTSU(imagen):
    if len(imagen.shape) > 2 and imagen.shape[2] == 3:  # imagen en color
        if not (np.array_equal(imagen[:,:,0], imagen[:,:,1]) and np.array_equal(imagen[:,:,1], imagen[:,:,2])): # canales de color no son iguales
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            return imagen
    elif len(imagen.shape) == 2 or imagen.shape[2] == 1:  # imagen en escala de grises
        thresh_img = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # op. morfologica
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,2))
        imagen = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=1)

        # Invertir Imagen
        imagen = 255 - imagen
        return imagen
    else:
        raise ValueError("Formato de imagen no soportado")
      
#realiza dos binarizaciones, escoger una entre 0 y 1
def binarizacion(imagen, otsu=0):
    # Verificamos si otsu tiene valores válidos
    #bin_anv: 98,127
    #bin_otsu_rev:89:118

    if otsu not in [0, 1]:raise ValueError("El valor de otsu debe ser 0 o 1.")

    if otsu == 1:
       
       return cv2.threshold(imagen, 127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
       
    else:
       return cv2.threshold(imagen,95,255,cv2.THRESH_BINARY)

def findMatches(descriptoresObjeto,descriptoresBase):
  """Idealmente tener una base de datos de entrenamiento de los descripores base,
     para luego simplemente consultar estos datos y buscar coincidencias,"""   
    # Verificar que descriptoresObjeto y descriptoresBase son arreglos de NumPy y del tipo float32
    
  if not isinstance(descriptoresObjeto, np.ndarray) or not isinstance(descriptoresBase, np.ndarray):
    raise ValueError("Los descriptores deben ser arreglos de NumPy.")
  if descriptoresObjeto.dtype != np.float32 or descriptoresBase.dtype != np.float32:
    raise ValueError("Los descriptores deben ser del tipo np.float32.")
  
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
        #pts: puntos que forman un rectangulo en base a las medidas h y w de la imagen de referencia
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

        #tomar el conjunto de puntos (pts) de img2 y aplicar la trasnformacion de perspectiva de puntos con la MAtriz de homografia M
        #dst contiene conjuntos de puntos que encuadran el carnet
        dst = cv2.perspectiveTransform(pts,M)

        return dst, M, matchesMask
    else:
        print( "No se encuentran suficientes coincidencias- {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None

        return None

def cargarDescriptores(nombre):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(BASE_DIR, 'data', f'descriptores_{nombre}.pkl')
    
    # Verificar si el archivo existe
    if not os.path.exists(FILE_PATH):
        raise ValueError(f"Archivo descriptores_{nombre}.pkl no encontrado.")
    
    # Cargar los descriptores del archivo
    with open(FILE_PATH, 'rb') as f:
        data = pkl.load(f)
    
    return data[nombre]    

def cargarKeypoints(lado):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(BASE_DIR, 'data', f'keypoints_{lado}.pkl')

    # Verificar si el archivo existe
    if not os.path.exists(FILE_PATH):
        raise ValueError(f"Archivo keypoints_{lado}.pkl no encontrado.")

    # Cargar los keypoints de un archivo pickle
    with open(FILE_PATH, 'rb') as file:
        keypoints = pkl.load(file)

    return keypoints
        
def guardarDescriptores():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_names = ["anverso", "reverso"]

    for name in image_names:
        # Buscando la imagen independientemente del formato
        found_images = glob.glob(os.path.join(BASE_DIR, 'data', f'{name}.*'))
        if not found_images:
            print(f"Imagen {name} no encontrada.")
            continue

        # Tomando la primera imagen encontrada (en caso de múltiples formatos, considera ajustar)
        IMAGE_PATH = found_images[0]
        image = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"La imagen {IMAGE_PATH} no se cargó correctamente.")

        sift = cv2.SIFT_create()
        kp, descriptores = sift.detectAndCompute(image, None)
        
        dic = {name: descriptores}
        SAVE_PATH = os.path.join(BASE_DIR, 'data', f'descriptores_{name}.pkl')
        with open(SAVE_PATH, 'wb') as f:
            pkl.dump(dic, f)     

def identificador_lado(img_side,tipo=''):
    min_matches=20
    
    #se define la cantidad minimas de coincidencias para cada lado
    if tipo=='anverso':
        min_matches=20
    elif tipo=='reverso':
        min_matches=8
    else:
        raise ValueError(f"Tipo de lado {tipo} no válido.")

    def matches(descriptorBase,descriptorObjetivo):
        if descriptorBase is None or descriptorObjetivo is None:
            return False

        # Busco los descriptores que están más cerca (brute force matcher)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptorBase, descriptorObjetivo, k=2)

        # Aplico test de cercanía
        good = []
        for m,n in matches:
            if m.distance < 0.5*n.distance:
                good.append([m])

        coincidencias = len(good)

        if (coincidencias > min_matches):
            print(f'Número de coincidencia de descriptores {tipo}: {coincidencias} > {min_matches}')
            return True
        else:
            return False
    
    ##########################################

    #cargar descriotires
    try:
        descriptores_base = cargarDescriptores(tipo)
    except ValueError as e:
        print(e)
        return False

    # Calculo los descriptores de la imagen nueva
    # Inicializo el detector SIFT
    # Query Image

    sift = cv2.SIFT_create()

    # Encuentro los descriptores de la imagen a revisar
    kp1, des1 = sift.detectAndCompute(img_side,None)

    suficientes_matches=matches(descriptores_base,des1)

    return suficientes_matches

def keypoints_descriptores(image):
  
  sift = cv2.SIFT_create(0, 3, 0.04, 0, 2)
  keypoints, descriptors = sift.detectAndCompute(image,None)
  return keypoints, descriptors

def abrir_Imagen(lado):
    imagen_numpy=None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_names = [lado]
    for name in image_names:
        found_images = glob.glob(os.path.join(BASE_DIR, 'data', f'{name}.*'))
        if not found_images:
            print(f"Imagen {name} no encontrada.")
            continue

        IMAGE_PATH = found_images[0]
        image = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"La imagen {IMAGE_PATH} no se cargó correctamente.")
        try:
            imagen_numpy=preparacionInicial(cv2.imread(IMAGE_PATH))
        except Exception as e:
            print(f"Error al abrir imagen: {e}")
    print(imagen_numpy)

    return imagen_numpy

def guardar_keypoints(keypoints, name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAVE_PATH = os.path.join(BASE_DIR, 'data', f'keypoints_{name}.pkl')

    try:
        with open(SAVE_PATH, 'wb') as f:
            pkl.dump(keypoints, f)
    except Exception as e:
        print(f"Error al guardar keypoints: {e}")

#usar metodo de matriz dde homografia para encuadrar la imagen
def encuadre(imagen,lado):
    descriptores_lado= cargarDescriptores(lado)
    MIN_MATCH_COUNT=20
    porc_calc_homografia=necesita_homografia(imagen,descriptores_lado,lado)

    if not porc_calc_homografia:
        return imagen,False
    else:
    
        kp_carnet, des_carnet = keypoints_descriptores(imagen)
        good=findMatches(des_carnet,descriptores_lado)
        imagen_ref=abrir_Imagen(lado)
        print(imagen_ref)
        keypoints_ref=cargarKeypoints(lado)
        dst, M, matchesMask=calcHomografia(good,MIN_MATCH_COUNT,imagen_ref,kp_carnet,keypoints_ref,imagen)
        h,w=imagen_ref.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        warped_img = cv2.warpPerspective(imagen, np.linalg.inv(M), (w, h))
        cv2.imwrite(f'warped_img{lado}.jpg', warped_img)

        return warped_img,True

def necesita_homografia(imagen, descriptores_lado,lado,umbral_anverso=0.3,umbral_reverso=0.1):
    kp_imagen, descriptores = keypoints_descriptores(imagen)
    
    # Aquí podrías usar la función findMatches o cualquier otra lógica para comparar los keypoints
    good_matches = findMatches(descriptores, descriptores_lado)
    
    # Si el porcentaje de buenos matches es menor que el umbral, se calcula la homografía
    print(f'Buenos Matches: {len(good_matches)} entre descriptores')
    print(f'{lado}, datos Img Objetivo: len(kps)={len(kp_imagen)}, len(descriptores)={len(descriptores)})')
    print(f'Numero de descriptores Base: {len(descriptores_lado)}')
    print(f'calculo: {len(good_matches)} / {len(descriptores_lado)}= {len(good_matches)/len(descriptores_lado)}')
    print('')
    if(lado=='anverso'):
        
        return len(good_matches)/len(descriptores_lado)< umbral_anverso
    else:
        return len(good_matches)/len(descriptores_lado)< umbral_reverso


