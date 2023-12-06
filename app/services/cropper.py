import cv2 as cv2
import numpy as np

def recortes_anverso(rut_bin):
    # 530x840
    rut_bin=escalar_imagen(rut_bin,530,840)
    estado_inicial = locals().copy()
    #anverso
    nombres = rut_bin[171:211 , 285:806]
    apellidos = rut_bin[93:157 , 283:806]
    
    RUN = rut_bin[453:496 , 98:273]
    nacionalidad = rut_bin[220:265, 285:425]
    sexo = rut_bin[222:263, 450:600]
    fecha_nacimiento = rut_bin[279:311 , 270:475]
    numero_documento = rut_bin[277:315, 470:663]
    fecha_emision = rut_bin[330:366, 270:470]
    fecha_vencimiento = rut_bin[328:370 , 472:663]
  
    estado_final = locals().copy()
    resultado_recortes = {k: estado_final[k] for k in estado_final if k not in estado_inicial and k not in ['estado_inicial', 'estado_final']}
    return resultado_recortes
    

def recortes_reverso(rut_bin2):
    rut_bin2=escalar_imagen(rut_bin2,530,840)
    
    #reverso
    estado_inicial = locals().copy()

    ciudad = rut_bin2[211:247 , 182:600]
    profesion = rut_bin2[242:274,182:403]
    profesion=rut_bin2[242:274 , 182:403]

    #recortar la tres lineas MRZ
    mrz_linea1=rut_bin2[343:398 , 37:495]
    mrz_linea2=rut_bin2[390:436 , 37:800]
    mrz_linea3=rut_bin2[432:482 , 37:800]

    linea1=mrz_linea1
    linea2=mrz_linea2
    linea3=mrz_linea3

    textoGeneral_MRZ = None
    mrz_raw=None

    nombres_MRZ = rut_bin2[440:482, 418:806]
    apellidos_MRZ = rut_bin2[440:478, 44:375]
    RUN_MRZ = rut_bin2[395:440,495:747]
    numeroDocumento_MRZ = rut_bin2[354:398,170:400]

    # Guarda el estado final después de hacer los recortes
    estado_final = locals().copy()

    # Crea un diccionario para las variables de recortes
    # Resta los estados para obtener solo las variables que se asignaron
    resultado_recortes = {k: estado_final[k] for k in estado_final if k not in estado_inicial and k not in ['estado_inicial', 'estado_final']}



    return resultado_recortes

def escalar_imagen(img, altura, anchura):
    
    if not isinstance(img, np.ndarray):
        raise ValueError("El parámetro 'img' debe ser un objeto numpy.ndarray.")
    
    return cv2.resize(img, (anchura, altura))

