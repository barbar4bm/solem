import cv2 as cv2
import pytesseract
import numpy as np

def obtenerTexto(imagenes, nombres=None):
    # Si "imagenes" es solo una imagen (verificando si es un ndarray de numpy y no una lista)
    if isinstance(imagenes, np.ndarray):
        return pytesseract.image_to_string(imagenes, lang="spa").strip()
    
    # Si "imagenes" es una lista de imágenes
    elif isinstance(imagenes, list) and all([isinstance(img, np.ndarray) for img in imagenes]):
        # Verificar si las longitudes de las listas son iguales
        if len(imagenes) != len(nombres):
            raise ValueError("La lista de imágenes y la lista de nombres deben tener la misma longitud.")
        
        # Diccionario para almacenar los resultados
        resultado = {}

        # Recorre las imágenes y extrae el texto
        for i, imagen in enumerate(imagenes):
            texto = pytesseract.image_to_string(imagen, lang="spa").strip()
            resultado[nombres[i]] = texto

        return resultado
    
    else:
        raise TypeError("El argumento 'imagenes' debe ser un ndarray o una lista de ndarrays.")

def assign_values_from_dict(obj, attributes_dict):
    # Comprobación inicial: asegurarse de que la cantidad de atributos del objeto y
    # la cantidad de elementos en el diccionario son los mismos
    if len(vars(obj)) != len(attributes_dict):
        raise ValueError("La cantidad de atributos del objeto y el tamaño del diccionario no coinciden.")

    # Asegurarse de que los nombres de los atributos en el objeto coincidan con las claves en el diccionario
    if set(vars(obj).keys()) != set(attributes_dict.keys()):
        raise ValueError("Los nombres de los atributos del objeto y las claves del diccionario no coinciden.")

    # Asignar valores desde el diccionario a los atributos del objeto
    for key, value in attributes_dict.items():
        setattr(obj, key, value)