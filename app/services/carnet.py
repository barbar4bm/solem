class Cedula:
    def __init__(self, datos_iniciales=None):
        # Define la estructura inicial con valores por defecto
        self.RUN = ""
        self.apellidos = ""
        self.nombres = ""
        self.nacionalidad = ""
        self.sexo = ""
        self.fecha_nacimiento = ""
        self.fecha_emision = ""
        self.fecha_vencimiento = ""
        self.numero_documento = ""
        self.ciudad = ""
        self.profesion = ""
        self.mrz = {
            "tieneMRZ": False,
            "datosMRZ": {
                "textoGeneral_MRZ": "",#separados por espacios
                "codigoPais_MRZ": "", 
                "nombres_MRZ": "",
                "RUN_MRZ": "",
                "numeroDocumento_MRZ": "",
                "apellidos_MRZ": "",
                "nacionalidad_MRZ": "",
                "sexo_MRZ": "",
                "fechaNacimiento_MRZ": "",
                "fechaVencimiento_MRZ": "",
            }
        }
        self.qr = ""

        # Si se proporciona un diccionario, actualiza los atributos con los valores correspondientes
        if isinstance(datos_iniciales, dict):
            self.actualizar_desde_dicionario(datos_iniciales)

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
            for key, value in data['mrz'].items():
                if key in self.mrz['datosMRZ']:
                    self.mrz['datosMRZ'][key] = value
            self.mrz["tieneMRZ"] = True
                

    def actualizar_datos_mrz(self, datos_actualizacion):
        for clave, valor in datos_actualizacion.items():
            if clave in self.mrz["datosMRZ"]:
                self.mrz["datosMRZ"][clave] = valor
        self.mrz["tieneMRZ"] = True


"""declarar una funcion que realize validaciones de los datos de la cedula
def validar_datos(self): la funcion me retorna un diccionari con una estructura que muestte los datos 
necesarios para saber si los campos coinciden..."""