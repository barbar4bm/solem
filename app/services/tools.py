import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import base64 as b64
import os
import json

def b64_openCV(imgenb64):
    try:
        # Decodificar el string base64 y convertirlo en una matriz numpy
        im_bytes = b64.b64decode(imgenb64)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # Verificar la validez de la imagen
        if imagen_valida(img):
            return img
        else:
            print("La imagen decodificada es inválida.")
            return None

    except b64.binascii.Error as e:
        print(f"Error de decodificación base64: {e}")
        return None
    except cv2.error as e:
        print(f"Error de OpenCV: {e}")
        return None
    except Exception as e:
        print(f"Error durante la decodificación de la imagen: {e}")
        return None

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

def imagen_valida(image): 
    try:
        # Intentar realizar operaciones básicas en la imagen
        # para verificar su integridad
        # Puedes personalizar esta verificación según tus necesidades específicas
        # Por ejemplo, verificar la forma de la matriz, el tipo de datos, etc.
        return image is not None and image.shape[0] > 0 and image.shape[1] > 0
    except Exception as e:
        # Si hay algún error durante el proceso, considerar la imagen como no válida
        return False

def leerQR(image):

    # Inicializar el detector de códigos QR con OpenCV
    qr_code_detector = cv2.QRCodeDetector()

    # Si no es un arreglo de numpy, lanzar una excepción
    if not isinstance(image, np.ndarray):
        raise ValueError("El argumento 'image' debe ser un arreglo de numpy (imagen de OpenCV).")
    
    # Detectar y decodificar el código QR
    value, pts, qr_code = qr_code_detector.detectAndDecode(image)
    return value
    
def numpy_to_png(imagen_np):
    """Convierte una matriz numpy a bytes de imagen PNG."""
    retval, buffer_png = cv2.imencode('.png', imagen_np)
    png_bytes = buffer_png.tobytes()
    return png_bytes

def escalar_imagen(img, altura, anchura):
    
    if not isinstance(img, np.ndarray):
        raise ValueError("El parámetro 'img' debe ser un objeto numpy.ndarray.")
    
    return cv2.resize(img, (anchura, altura))


def b64_imagen(imagen):
    # Decodificar la cadena base64 a bytes
    img_bytes = b64.b64decode(imagen)

    # Convertir los bytes a una matriz numpy
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)

    # Decodificar la matriz a una imagen
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Guardar la imagen como un archivo jpg
    cv2.imwrite('imagen.jpg', img)

def cargar_diccionario_paises():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DICT_FILE_PATH = os.path.join(BASE_DIR, 'data', 'dic_paises.json')

    # Verificar si el archivo existe
    if not os.path.exists(DICT_FILE_PATH):
        raise ValueError("Archivo dic_paises.json no encontrado.")

    # Cargar el diccionario desde el archivo
    with open(DICT_FILE_PATH, 'r') as f:
        dic_paises = json.load(f)

    return dic_paises

def cargar_trat_nacionalidades():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DICT_FILE_PATH = os.path.join(BASE_DIR, 'data', 'dic_trat_nacional.json')

    # Verificar si el archivo existe
    if not os.path.exists(DICT_FILE_PATH):
        raise ValueError("Archivo dic_trat_nacional.json no encontrado.")

    # Cargar el diccionario desde el archivo
    with open(DICT_FILE_PATH, 'r') as f:
        dic_trat_nacional = json.load(f)

    return '' if dic_trat_nacional is None else dic_trat_nacional

def cargarPaises():
    # Este es un ejemplo de cómo podrías definir las rutas de archivo si __file__ no está disponible
    # En un script real, deberías usar __file__ para obtener la ruta base
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(BASE_DIR, 'data', 'paises_procesados.txt')
    DICT_FILE_PATH = os.path.join(BASE_DIR, 'data', 'dic_paises.json')

    # Verificar si el archivo existe
    if not os.path.exists(FILE_PATH):
        raise ValueError("Archivo paises_procesados.txt no encontrado.")

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # Crear el diccionario
    dic_paises = {}
    for linea in lineas:
        # Dividir la línea en el nombre del país y la abreviatura
        try:
            nombre_pais, abreviatura_pais = linea.strip().split('/')
            dic_paises[abreviatura_pais] = nombre_pais
        except ValueError:
            print(f"Error al procesar la línea: {linea.strip()}")
            continue  # Omitir esta línea y continuar con la siguiente

    # Guardar el diccionario en un archivo
    with open(DICT_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(dic_paises, f, ensure_ascii=False, indent=4)

    return dic_paises

def mostrar_imagen(imagen, titulo='Imagen'):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)

def mostrar_imagen_plt(imagen):
    plt.imshow(imagen, cmap='gray')
    plt.title('imagen')
    plt.show()

def convertir_diccionario_a_base64(diccionario_img, claves_omitidas=None):
    diccionario_base64 = {}
    for clave, imagenOpenCV in diccionario_img.items():
        # Comprobar si la clave está en la lista de claves omitidas y si la imagen no está vacía
        if (claves_omitidas is None or clave not in claves_omitidas) and (imagenOpenCV is not None and imagenOpenCV.size > 0):
            diccionario_base64[clave] = openCV_b64(imagenOpenCV)
    return diccionario_base64