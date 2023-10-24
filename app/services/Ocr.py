import cv2 as cv2
import pytesseract
import numpy as np

def obtenerTexto(dicc_imagenes):
    if not isinstance(dicc_imagenes, dict):
        raise TypeError("El argumento 'dicc_imagenes' debe ser un diccionario con nombres de atributos y imágenes.")

    # Diccionario para almacenar los resultados
    resultado = {}

    # Recorre las imágenes en el diccionario y extrae el texto
    for nombre, imagen in dicc_imagenes.items():
        # Verificar que la imagen sea un ndarray de numpy
        if not isinstance(imagen, np.ndarray):
            raise TypeError(f"La imagen asociada con '{nombre}' no es un ndarray válido.")
        
        texto = pytesseract.image_to_string(imagen, lang="spa").strip()
        resultado[nombre] = texto

    return resultado

def Asignar_Valores_Objeto(obj, attributes_dict):
    # Asignar valores desde el diccionario a los atributos del objeto si el atributo existe en el objeto
    for key, value in attributes_dict.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
        else:
            print(f"Advertencia: El objeto no tiene el atributo '{key}'. El valor no fue asignado.")