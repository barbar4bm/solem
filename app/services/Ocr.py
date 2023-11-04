import cv2 as cv2
import pytesseract
import numpy as np
from . import tools as tool

def obtenerTexto(dicc_imagenes, *claves_omitidas):
    if not isinstance(dicc_imagenes, dict):
        raise TypeError("El argumento 'dicc_imagenes' debe ser un diccionario con nombres de atributos y imágenes.")

    # Convertir claves_omitidas en un conjunto para hacer la comprobación más eficiente
    claves_omitidas = set(claves_omitidas)

    # Diccionario para almacenar los resultados
    resultado = {}

    # Recorre las imágenes en el diccionario y extrae el texto
    for nombre, imagen in dicc_imagenes.items():
        # Si la clave actual está en claves_omitidas, añadimos la imagen al resultado y saltamos esta iteración
        #en este caso se lee el qr, ya que no se puede aplciar OCR al QR
        if nombre in claves_omitidas:
            if nombre=="qr":
                resultado[nombre]=tool.leerQR(imagen)
                print(resultado[nombre])
                continue
                #se agregua elif para otros casos...

        # Verificar que la imagen sea un ndarray de numpy
        if not isinstance(imagen, np.ndarray):
            resultado[nombre] = "Imagen ilegible"
            continue
        
        texto = pytesseract.image_to_string(imagen).strip()
        
        # Eliminar saltos de línea
        texto = texto.replace("\n", "")

        resultado[nombre] = texto

    return resultado

def Asignar_Valores_Objeto(obj, attributes_dict):
    # Asignar valores desde el diccionario a los atributos del objeto si el atributo existe en el objeto
    for key, value in attributes_dict.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
        else:
            print(f"Advertencia: El objeto no tiene el atributo '{key}'. El valor no fue asignado.")


