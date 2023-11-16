from services.carnet import Cedula

def procesar_validaciones(carnet, porcentaje_de_aprobar=0.8):
    nacionalidad = comparar_nacionalidad(carnet, porcentaje_de_aprobar)
    nombre_completo = comparar_nombre_completo(carnet, porcentaje_de_aprobar)
    fecha_nacimiento = comparar_fecha(carnet, 'nacimiento', porcentaje_de_aprobar)
    fecha_vencimiento = comparar_fecha(carnet, 'vencimiento', porcentaje_de_aprobar)
    numero_documento = comparar_num_documento(carnet, porcentaje_de_aprobar)
    run=comparar_RUN(carnet, porcentaje_de_aprobar)

    return {
        'comparar_nacionalidad': nacionalidad,
        'comparar_nombre_completo': nombre_completo,
        'comparar_fecha_nacimiento': fecha_nacimiento,
        'comparar_fecha_vencimiento': fecha_vencimiento,
        'comparar_numero_documento': numero_documento,
        'comparar_RUN':run
    }


def comparar_nacionalidad(carnet, porcentaje_de_aprobar=0.8):
    if 'nacionalidad_MRZ' not in carnet.mrz['datosMRZ'] or not hasattr(carnet, 'nacionalidad'):
        return False
    nacionalidad_back = carnet.mrz['datosMRZ']['nacionalidad_MRZ']
    nacionalidad_front = carnet.nacionalidad
    return calcular_coincidencia(nacionalidad_front, nacionalidad_back, porcentaje_de_aprobar)

def comparar_nombre_completo(carnet, porcentaje_de_aprobar=0.8):
    if 'apellidos_MRZ' not in carnet.mrz['datosMRZ'] :
        return False
    nombre = (carnet.apellidos + carnet.nombres).replace(" ", "")
    nombre_mrz = (carnet.mrz['datosMRZ']['apellidos_MRZ']+carnet.mrz['datosMRZ']['nombres_MRZ']).replace(" ", "")

    print(nombre,'',nombre_mrz)
    return calcular_coincidencia(nombre, nombre_mrz, porcentaje_de_aprobar)

def comparar_fecha(carnet, tipo_fecha, porcentaje_de_aprobar=0.8):

    if tipo_fecha not in ['nacimiento', 'vencimiento']:
        return False
    else:
        fecha_front=None
        fecha_back=None
        if(tipo_fecha=='nacimiento'):
            if hasattr(carnet, 'fecha_nacimiento') and 'fechaNacimiento_MRZ' in carnet.mrz['datosMRZ']:
                fecha_front=carnet.fecha_nacimiento
                fecha_back=carnet.mrz['datosMRZ']['fechaNacimiento_MRZ']
            else:
                return False
        elif(tipo_fecha=='vencimiento'):
            if hasattr(carnet, 'fecha_vencimiento') and 'fechaVencimiento_MRZ' in carnet.mrz['datosMRZ']:
                fecha_front=carnet.fecha_vencimiento
                fecha_back=carnet.mrz['datosMRZ']['fechaVencimiento_MRZ']
            else:
                return False
        return calcular_coincidencia(fecha_front, fecha_back, porcentaje_de_aprobar)

def comparar_num_documento(carnet, porcentaje_de_aprobar=0.8):
    if not hasattr(carnet,'numero_documento') or 'numeroDocumento_MRZ' not in carnet.mrz['datosMRZ']:
        return False
    numero_documento_front = carnet.numero_documento
    numero_documento_back = carnet.mrz['datosMRZ']['numeroDocumento_MRZ']
    return calcular_coincidencia(numero_documento_front, numero_documento_back, porcentaje_de_aprobar)

def calcular_coincidencia(dato1, dato2, porcentaje_de_aprobar):
    if dato1 is None or dato2 is None or len(dato1) == 0:
        return False
    contar = sum(1 for a, b in zip(dato1, dato2) if a == b)
    calcular = contar / len(dato1)
    return calcular >= porcentaje_de_aprobar

def comparar_RUN(carnet, porcentaje_de_aprobar):
    if not hasattr(carnet,'RUN') or 'RUN_MRZ' not in carnet.mrz['datosMRZ']:
        return False
    RUN_front = carnet.RUN
    RUN_back = carnet.mrz['datosMRZ']['RUN_MRZ']
    return calcular_coincidencia(RUN_front, RUN_back, porcentaje_de_aprobar)


