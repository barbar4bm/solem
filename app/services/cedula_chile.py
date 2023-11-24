import os
import platform
import pytesseract
from services import cropper
from services import Ocr,tools
from services import Sift as sift
from services.carnet import Cedula
from services import validacion as validar


def esWin():
    # Rutas posibles del ejecutable de Tesseract OCR en Windows
    tesseract_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',  # Ubicación común en Windows 64 bits
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'  # Ubicación común en Windows 32 bits
    ]

    # Verificar si el sistema operativo es Windows
    if platform.system() == 'Windows':
        # Buscar el ejecutable en las rutas posibles
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break


def procesar_imgenes_cedula(data):
    # Convertir las imágenes de base64 a objetos de imagen
    anverso=tools.b64_openCV(data['anverso'])
    reverso=tools.b64_openCV(data['reverso'])

    anverso_filtr=sift.preparacionInicial(anverso,'anverso')
    reverso_filtr=sift.preparacionInicial(reverso,'reverso')
    
    resp_Anverso=sift.identificador_lado(anverso_filtr,'anverso')
    resp_reverso=sift.identificador_lado(reverso_filtr,'reverso')

    #atratapar cuando alguno es falso y generar jSON respuesta
    #aqui se llama a alguna funcion de codeJSON

    """    
    if not resp_Anverso:
        return {'ocr_data': 'No se reconoce como cédula chilena'}"""
            
    resp_Anverso=str(resp_Anverso)
    resp_reverso=str(resp_reverso)

    """
    anv_img_hom,resp_anv_bool=sift.encuadre(anverso_filtr,'anverso')
    rev_img_hom,resp_anv_bool=sift.encuadre(reverso_filtr,'reverso')"""


    #SEPAR LOS RECORTES, EN CROPpER LA FUNCION RECORTES SE DIVIDE EN DOS
    #unir los diccioanrios para inserten al objeto 
    diccionario_anverso=cropper.recortes_anverso(anverso)
    diccionario_reverso=cropper.recortes_reverso(reverso)
    
    clave_omitida=('textoGeneral_MRZ','mrz_raw')
    diccionario_anverso=sift.preparacionInicial(diccionario_anverso,'anverso',clave_omitida,'procesar_imagen')
    diccionario_reverso=sift.preparacionInicial(diccionario_reverso,'reverso',clave_omitida,'bin_OTSU')
    

    diccionario_img={**diccionario_anverso,**diccionario_reverso}
    tools.guardar_recortes(diccionario_anverso,'anverso')
    tools.guardar_recortes(diccionario_reverso,'reverso')

    clave_omitida=('textoGeneral_MRZ','mrz_raw','linea1','linea2','linea3')
    #se retornan tupla, [0]: textos reconocidos, [1]: claves de texto no reconocidass
    dic_ocr=Ocr.obtenerTexto(diccionario_img,*clave_omitida)[0]
    carnet=Cedula(dic_ocr)
    ocr_data=vars(carnet)
    #verificaciones
    dic_validaciones=validar.procesar_validaciones(carnet)

    datos_respuesta = {'dic_validaciones': dic_validaciones,'ocr_data':ocr_data, 'reconoce_Anverso': resp_Anverso, 'reconoce_Reverso': resp_reverso}

    return datos_respuesta
