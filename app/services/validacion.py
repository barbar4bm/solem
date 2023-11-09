from services.carnet import Cedula

def procesar_validaciones(carnet):
    #datos anverso
    nacionalidad_anverso=carnet.nacionalidad
    nombre_completo=carnet.nombres+carnet.apellidos
    fecha_nacimiento=carnet.fecha_nacimiento 
    numero_documento=carnet.numero_documento

    #datos reverso
    if(carnet.mrz['tieneMRZ']):
      dic_mrz=carnet.mrz['datosMRZ']
      nacionalidad_reverso=dic_mrz['nacionalidad_MRZ']




def comparar_nacionalidad(nacionalidad_front,nacionalidad_back,porcentaje_de_aprobar):
    calcular = 0
    contar = 0
    for i in range(len(nacionalidad_back)):
        if (nacionalidad_front[i] == nacionalidad_back[i]):
            contar = contar + 1
        else:
            return False
        calcular = contar / len(nacionalidad_front)
    if (calcular >= porcentaje_de_aprobar):
        return True
    else:
        return False

def comparar_nombre_completo(nombre , arreglo, porcentaje_de_aprobar):
    calcular = 0
    contar = 0
    for i in range(len(arreglo[0])):
        datos_mrz = arreglo[0]
        if (nombre[i] == datos_mrz[i]):
            contar = contar + 1
        else:
            return False
        calcular = contar / len(nombre)
    if (calcular >= porcentaje_de_aprobar):
        return True
    else:
        return False
    
def comparar_fecha(fecha_front,fecha_back,umbral):
    porcentaje_de_aprobar = umbral
    calcular = 0
    contar = 0
    for i in range(len(fecha_back)):
        if (fecha_front[i] == fecha_back[i]):
            contar = contar + 1
        else:
            return False
        calcular = contar / len(fecha_front)
    if (calcular >= porcentaje_de_aprobar):
        return True
    else:
        return False
    
def comparar_documentos(front,back,porcentaje_de_aprobar): 
    calcular = 0
    contar = 0
    for i in range(len(back)):
        if (front[i] == back[i]):
            contar = contar + 1
        else:
            return False
        calcular = contar / len(front)
    if (calcular >= porcentaje_de_aprobar):
        return True
    else:
        return False