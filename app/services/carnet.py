class Cedula:
    def __init__(self, 
                 RUN="", 
                 apellidos="", 
                 nombres="", 
                 nacionalidad="", 
                 sexo="", 
                 fecha_nacimiento="", 
                 fecha_emision="", 
                 fecha_vencimiento="", 
                 numero_documento="",
                 ciudad="",
                 profesion="",
                 mrz=None,  # Esto será un diccionario
                 qr=""):
        
        self.RUN = RUN
        self.apellidos = apellidos
        self.nombres = nombres
        self.nacionalidad = nacionalidad
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_emision = fecha_emision
        self.fecha_vencimiento = fecha_vencimiento
        self.numero_documento = numero_documento
        self.ciudad = ciudad
        self.profesion = profesion
        self.mrz={
            "tieneMRZ": False,
            "datosMRZ": {
                "textoGeneral": "",
                "codigoPais": "",
                "nombres": "",
                "RUN":"",
                "numeroDocumento": "",
                "nombres": "",
                "apellidos": "",
                "nacionalidad": "",
                "sexo": "",
                "fechaNacimiento": "",
                "fechaVencimiento": "",
            }
        }
        self.qr = qr

    def __str__(self):
        return (f"RUN: {self.RUN}\n"
                f"Apellidos: {self.apellidos}\n"
                f"Nombres: {self.nombres}\n"
                f"Nacionalidad: {self.nacionalidad}\n"
                f"Sexo: {self.sexo}\n"
                f"Fecha de Nacimiento: {self.fecha_nacimiento}\n"
                f"Fecha de Emisión: {self.fecha_emision}\n"
                f"Fecha de Vencimiento: {self.fecha_vencimiento}\n"
                f"Numero de Documento: {self.numero_documento}\n"
                f"Ciudad: {self.ciudad}\n"
                f"Profesión: {self.profesion}\n"
                f"MRZ: {self.mrz}\n"
                f"QR: {self.qr}\n")
    
    #keys_to_update es una lista ['','',''] de claves que se deben actualizar.
    def actualizar_desde_dicionario(self, data, keys_to_update=None):
        # Si se proporciona keys_to_update, solo se actualizan esos claves.
        # De lo contrario, se actualizan todas las claves que coincidan.
        if keys_to_update is not None:
            data = {key: data[key] for key in keys_to_update if key in data}
        
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        # Actualizar el MRZ si es necesario
        if 'mrz' in data and isinstance(data['mrz'], dict):
            self.mrz.update(data['mrz'])

"""declarar una funcion que realize validaciones de los datos de la cedula
def validar_datos(self): la funcion me retorna un diccionari con una estructura que muestte los datos 
necesarios para saber si los campos coinciden..."""