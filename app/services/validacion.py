from services.carnet import Cedula

def procesar_validaciones1(carnet, porcentaje_de_aprobar=0.8):
    nacionalidad = comparar_nacionalidad(carnet, porcentaje_de_aprobar)
    nombre_completo = comparar_nombre_completo(carnet, porcentaje_de_aprobar)
    """
    
    fecha_nacimiento = comparar_fecha(carnet, 'nacimiento', porcentaje_de_aprobar)
    fecha_vencimiento = comparar_fecha(carnet, 'vencimiento', porcentaje_de_aprobar)
    numero_documento = comparar_num_documento(carnet, porcentaje_de_aprobar)  

    """

    print(nacionalidad,nombre_completo)

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
    print(nombre,' ',nombre_mrz)
    return calcular_coincidencia(nombre, nombre_mrz, porcentaje_de_aprobar)

def comparar_fecha(carnet, tipo_fecha, porcentaje_de_aprobar=0.8):
    if tipo_fecha not in ['nacimiento', 'vencimiento']:
        return False
    fecha_front = carnet.get(f'fecha_{tipo_fecha}', None)
    fecha_back = carnet.mrz['datosMRZ'].get(f'fecha{tipo_fecha.capitalize()}_MRZ', None)
    if not fecha_front or not fecha_back:
        return False
    return calcular_coincidencia(fecha_front, fecha_back, porcentaje_de_aprobar)

def comparar_num_documento(carnet, porcentaje_de_aprobar=0.8):
    if 'numero_documento' not in carnet or 'numeroDocumento_MRZ' not in carnet.mrz['datosMRZ']:
        return False
    numero_documento_front = carnet['numero_documento']
    numero_documento_back = carnet.mrz['datosMRZ']['numeroDocumento_MRZ']
    return calcular_coincidencia(numero_documento_front, numero_documento_back, porcentaje_de_aprobar)

def calcular_coincidencia(dato1, dato2, porcentaje_de_aprobar):
    contar = sum(1 for a, b in zip(dato1, dato2) if a == b)
    calcular = contar / len(dato1)
    return calcular >= porcentaje_de_aprobar

def comparar_con_qr(carnet):
    pass