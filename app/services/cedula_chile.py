import os
import platform
import pytesseract
from services import gvision
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

    anverso_cp=anverso.copy()
    anverso_cp=sift.preparacionInicial(anverso_cp)  
    reverso=tools.b64_openCV(data['reverso'])


    anverso_filtr=sift.preparacionInicial(anverso)
    reverso_filtr=sift.preparacionInicial(reverso)
    resp_Anverso,resp_reverso=sift.identificador_lado(anverso_filtr,'anverso'),sift.identificador_lado(reverso_filtr,'reverso')
    _=None
    resp_anv=None
    resp_rev=None
    if resp_Anverso and resp_reverso:
        pic_anv,resp_anv=sift.encuadre(anverso_filtr,'anverso')
        anverso=pic_anv
        pic_rev,resp_rev=sift.encuadre(reverso_filtr,'reverso')
        reverso=pic_rev
    elif not resp_Anverso and resp_reverso:
        pic_anv,resp_anv=sift.encuadre(anverso_filtr,'anverso')
        anverso=pic_anv
    elif resp_Anverso and not resp_reverso:
        pic_rev,resp_rev=sift.encuadre(reverso_filtr,'reverso')
        reverso=pic_rev


        #atratapar cuando alguno es falso y generar jSON respuesta
        #aqui se llama a alguna funcion de codeJSON


    if resp_Anverso and not resp_reverso:
        return {'ocr_data': 'Solo se reconoce Anverso'}
    elif not resp_Anverso and resp_reverso:
        return {'ocr_data': 'Solo se reconoce Reverso'}
    elif not resp_Anverso and not resp_reverso:
        return {'ocr_data': 'No se reconoce como Cedula'}


    resp_Anverso=str(resp_Anverso)
    resp_reverso=str(resp_reverso)

        #aplicar binarizacion de otsu al reverso par amejorar lectura con ocr
        #ret, img_otsu=sift.binarizacion(reverso,1)



    #SEPAR LOS RECORTES, EN CROPER LA FUNCION RECORTES SE DIVIDE EN DOS
    #unir los diccioanrios para inserten al objeto 
    diccionario_img=cropper.recorte(anverso,reverso)
   

    #Se recortan por separado anverso y reverso
    dic_img_anverso=cropper.recortes_anverso(anverso)
    dic_img_reverso=cropper.recortes_reverso(reverso)

    

    dic_img_anverso=sift.preparacionInicial(dic_img_anverso,None,'bin')
    dic_img_reverso=sift.preparacionInicial(dic_img_reverso,'qr','bin') #al reverso se le aplica binarizacion de otsu

    tools.guardar_recortes(dic_img_anverso,'anverso')
    tools.guardar_recortes(dic_img_reverso,'reverso-otsu')

    clave_omitida=('qr','textoGeneral_MRZ','mrz_raw','linea1','linea2','linea3')
    #se retornan tupla, [0]: textos reconocidos, [1]: claves de texto no reconocidass
    dic_ocr_anverso=Ocr.obtenerTexto(dic_img_anverso,*clave_omitida)[0]
    dic_ocr_reverso=Ocr.obtenerTexto(dic_img_reverso,*clave_omitida)[0]

    dic_ocr_carnet = {**dic_ocr_anverso, **dic_ocr_reverso}#se juntan los diccionarios en uno solo
    carnet=Cedula(dic_ocr_carnet)

    gvision.procesamiento_gvision(dic_img_anverso,carnet.mrz['datosMRZ']['nombres_MRZ']+'-anv')  
    gvision.procesamiento_gvision(dic_img_reverso,carnet.mrz['datosMRZ']['nombres_MRZ']+'-rev')



    gvision.procesamiento_gvision({'Front':anverso_cp},'frontal'+carnet.mrz['datosMRZ']['nombres_MRZ'])

    ocr_data=vars(carnet)
        

    #verificaciones
    dic_validaciones=validar.procesar_validaciones(carnet)

    datos_respuesta = {'dic_validaciones': dic_validaciones,'ocr_data':ocr_data, 'reconoce_Anverso': resp_Anverso, 'reconoce_Reverso': resp_reverso}

    return datos_respuesta
