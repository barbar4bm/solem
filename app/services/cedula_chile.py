from flask import Blueprint, render_template, request, jsonify,json
from services import Ocr,tools
from services import Sift as sift
from services import cropper
from services.carnet import Cedula
from services import validacion as validar

def procesar_imgenes_cedula(data):
    # Convertir las imágenes de base64 a objetos de imagen
    anverso=tools.b64_openCV(data['anverso'])
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



    diccionario_img=cropper.recorte(anverso,reverso)
    diccionario_img_prep1=sift.preparacionInicial(diccionario_img,'qr')
    tools.guardar_recortes(diccionario_img_prep1,'prepInicial')
    clave_omitida=('qr','textoGeneral_MRZ','mrz_raw','linea1','linea2','linea3')
    diccionario_ocr, no_rec = Ocr.obtenerTexto(diccionario_img_prep1, *clave_omitida)

    carnet=Cedula(diccionario_ocr)
    ocr_data=vars(carnet)
        

    #verificaciones
    dic_validaciones=validar.procesar_validaciones(carnet)

    datos_respuesta = {'dic_validaciones': dic_validaciones,'ocr_data':ocr_data, 'reconoce_Anverso': resp_Anverso, 'reconoce_Reverso': resp_reverso}

    return datos_respuesta