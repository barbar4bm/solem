import cv2 as cv2
import difflib
import pytesseract
import numpy as np
from . import tools as tool
from services import Sift
import re


def encontrar_coincidencia_aproximada(texto_ocr):
    diccionario = tool.cargar_trat_nacionalidades()
    # Usar get_close_matches para encontrar la coincidencia más cercana
    coincidencias = difflib.get_close_matches(texto_ocr, diccionario.keys(), n=1, cutoff=0.6)

    if coincidencias:
        # Retornar la primera coincidencia y su valor correspondiente en el diccionario
        clave_aproximada = coincidencias[0]
        return clave_aproximada, diccionario[clave_aproximada]
    else:
        # Si no se encuentra ninguna coincidencia, retornar None
        return None, None




#recibe un diccionario con imagenes
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
                print('primero',resultado[nombre])
                if resultado[nombre] =='':
                    cv2.imwrite('nomr.jpg', imagen)

                    hola=Sift.bin_INV_OTSU(imagen)
                    cv2.imwrite('imagen.jpg', hola)
                    resultado[nombre] = tool.leerQR(hola)
                    print('con otsu:',resultado[nombre])
                resultado['datos_qr']=tool.extraer_datos_qr(resultado[nombre])

                continue
            elif nombre=="linea1" or nombre=="linea2" or nombre=="linea3":
                    resultado[nombre]=pytesseract.image_to_string(imagen)
                    continue
            continue
                #se agregua elif para otros casos...

        # Verificar que la imagen sea un ndarray de numpy
        if not isinstance(imagen, np.ndarray):
            resultado[nombre] = "Imagen ilegible"
            continue
        
        texto = pytesseract.image_to_string(imagen)
       

        if(texto==''):
            texto=Sift.bin_INV_OTSU(imagen)
            texto=pytesseract.image_to_string(texto)
            print('con otsu:',texto)

        texto=limpiar_datos(texto,nombre)
        resultado[nombre] = texto

    return resultado

def Asignar_Valores_Objeto(obj, attributes_dict):
    # Asignar valores desde el diccionario a los atributos del objeto si el atributo existe en el objeto
    for key, value in attributes_dict.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
        else:
            print(f"Advertencia: El objeto no tiene el atributo '{key}'. El valor no fue asignado.")




def limpiar_datos(ocr_result,atributo=''):
    cleaned_data = re.sub('[^a-zA-Z0-9]', '', str(ocr_result))

    if atributo=='nacionalidad':
        cleaned_data = re.sub('[^A-Z]', '', str(cleaned_data))
        _,cleaned_data=encontrar_coincidencia_aproximada(cleaned_data)

    return cleaned_data


def aplicarOCR(imagen):
    # Verificar que la imagen sea un ndarray de numpy
    if not isinstance(imagen, np.ndarray):
        return {"error": "Imagen ilegible"}

    # Aplicar OCR a la imagen
    texto = pytesseract.image_to_string(imagen)

    # Devolver el resultado
    return {"resultado": texto}


