from services import Ocr,tools
from services import Sift as sift
from services import cropper
from services.carnet import Cedula
from services import validacion as validar
from services import graficos
from services import gvision
import json
import os

def procesamiento_gvision(diccionario_img):
    print('gvision')

    #convertir a b64 cada imagen

    dic_b64=tools.convertir_diccionario_a_base64(diccionario_img)
    diccionario=json.dumps(dic_b64,indent=4)
    with open('diccionario_base64.txt', 'w') as file:
        file.write(diccionario)

    
    # Obtener el directorio base (donde se encuentra el archivo Python actual)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta hacia ocr-gv.json
    archivo_credenciales = os.path.join(BASE_DIR, 'data', 'ocr-gv.json')
    # Verificar si el archivo existe
    existe_archivo = os.path.exists(archivo_credenciales)
    print(f"La ruta del archivo de credenciales es: {archivo_credenciales}")
    print(f"¿Existe el archivo de credenciales? {existe_archivo}")


    dic_respuesta=gvision.enviar_a_google_vision(dic_b64,archivo_credenciales)
    dic_text_rec=gvision.procesar_respuestas_vision(dic_respuesta,dic_b64.keys())
    print(dic_text_rec)

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



    #SEPAR LOS RECORTES, EN CROPER LA FUNCION RECORTES SE DIVIDE EN DOS
    #unir los diccioanrios para inserten al objeto 
    diccionario_img=cropper.recorte(anverso,reverso)
    procesamiento_gvision(diccionario_img)

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
    ocr_data=vars(carnet)
        

    #verificaciones
    dic_validaciones=validar.procesar_validaciones(carnet)

    datos_respuesta = {'dic_validaciones': dic_validaciones,'ocr_data':ocr_data, 'reconoce_Anverso': resp_Anverso, 'reconoce_Reverso': resp_reverso}

    return datos_respuesta
