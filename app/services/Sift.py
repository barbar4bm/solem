import pickle as pkl
import cv2 as cv2
import numpy as np
import os
import glob

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
        try:
            with open(SAVE_PATH, 'wb') as f:
                pkl.dump(dic, f)
        except Exception as e:
            print(f"Error al guardar descriptores: {e}")



def puntos_descriptores(image):
  sift = cv2.xfeatures2d.SIFT_create(0, 3, 0.04, 0, 2)
  puntos,descriptores=sift.detectAndCompute(image,None)
  return puntos,descriptores

#cambio a RGB,conv a escala grises, 
def preparacionInicial(imagenInicial):
  #de BGR a RGB
  imagenInicialRGB = cv2.cvtColor(imagenInicial, cv2.COLOR_BGR2RGB)
  # Cambio de espacio de color BGR a GRAY
  gray = cv2.cvtColor(imagenInicialRGB, cv2.COLOR_BGR2GRAY)
  # Ecualización "Contrast Limited Adaptive Histogram Equalization,
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
  eq=clahe.apply(gray)

  return eq

#realiza dos binarizaciones, escoger una entre 0 y 1
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

def identificador_lados(anverso,reverso):

    def matches(descriptorBase,descriptorObjetivo):
            # Busco los descriptores que están más cerca (brute force matcher)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptorBase, descriptorObjetivo, k=2)

        # Aplico test de cercanía
        good = []
        for m,n in matches:
            if m.distance < 0.5*n.distance:
                good.append([m])

        coincidencias = len(good)
        #print(f'Número de coincidencia de descriptores: {coincidencias}')


        if (coincidencias > 20):
            return True
        else:
            return False
    
    ##########################################

    #cargar descriotires
    desc_lado_anverso = cargarDescriptores('anverso')
    desc_lado_reverso = cargarDescriptores('reverso')


    # Calculo los descriptores de la imagen nueva
    # Inicializo el detector SIFT
    # Query Image

    sift = cv2.SIFT_create()

    # Encuentro los descriptores de la imagen a revisar
    kp1, des1 = sift.detectAndCompute(anverso,None)
    kp2, des2= sift.detectAndCompute(reverso,None)


    esAnverso=matches(desc_lado_anverso,des1)
    esReverso=matches(desc_lado_reverso,des2)

    return esAnverso,esReverso




def is_screen_image(img):
    coeffs2 = pywt.dwt2(img, 'bior1.3')
    LL, (LH, HL, HH) = coeffs2
    
    # Calcula la varianza o energía de las componentes de detalle
    energy_LH = np.sum(np.square(LH))
    energy_HL = np.sum(np.square(HL))
    energy_HH = np.sum(np.square(HH))
    
    threshold = 1e5  # Establecer un umbral adecuado basado en tu conjunto de datos
    if energy_LH > threshold or energy_HL > threshold or energy_HH > threshold:
        return True  # La imagen posiblemente fue tomada desde una pantalla
    return False

   
