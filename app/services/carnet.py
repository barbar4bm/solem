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
    
    def actualizar_desde_dicionario(self, data, keys_to_update=None):
        # Verifica si las claves MRZ específicas están en el diccionario y tienen contenido
        claves_mrz = ['mrz_linea1', 'mrz_linea2', 'mrz_linea3']
        if all(clave in data and data[clave].strip() for clave in claves_mrz):
            # Construye el texto general MRZ y lo asigna
            self.mrz['datosMRZ']['textoGeneral_MRZ'] = " ".join(data[clave] for clave in claves_mrz)
            self.mrz['tieneMRZ'] = True
        
        # Si se proporciona keys_to_update, solo se actualizan esas claves.
        if keys_to_update is not None:
            data = {key: data[key] for key in keys_to_update if key in data}
        
        # Actualiza las demás claves proporcionadas en data
        for key, value in data.items():
            if hasattr(self, key) and key not in claves_mrz:  # Ignora las claves MRZ ya que ya se han procesado
                setattr(self, key, value)
                

    def actualizar_datos_mrz(self, datos_actualizacion):
        for clave, valor in datos_actualizacion.items():
            if clave in self.mrz["datosMRZ"]:
                self.mrz["datosMRZ"][clave] = valor
        self.mrz["tieneMRZ"] = True


"""declarar una funcion que realize validaciones de los datos de la cedula
def validar_datos(self): la funcion me retorna un diccionari con una estructura que muestte los datos 
necesarios para saber si los campos coinciden..."""