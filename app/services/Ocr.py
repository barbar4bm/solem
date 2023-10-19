import cv2 as cv2
import pytesseract

def obtenerTexto(imagenes, nombres):
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