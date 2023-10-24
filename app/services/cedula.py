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
        self.mrz=mrz
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