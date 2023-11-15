import re
from services import tools
from services import Ocr as ocr
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
                "mrz_raw":[],
                "textoGeneral_MRZ": "",#separados por espacios
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
        self.qr = "",
        self.datos_qr=None

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
        claves_mrz_raw=['linea1','linea2','linea3']

        if all(clave in data and data[clave].strip() for clave in claves_mrz):
            # Construye el texto general MRZ y lo asigna
            self.mrz['datosMRZ']['textoGeneral_MRZ'] = " ".join(data[clave] for clave in claves_mrz)
            self.mrz['tieneMRZ'] = True
            self.mrz['datosMRZ']['mrz_raw'] = [data[clave].replace('\n', '') for clave in claves_mrz_raw]
            # Procesa las líneas MRZ
            lineas_raw=self.mrz['datosMRZ']['mrz_raw']
            self.mrz['datosMRZ']['numeroDocumento_MRZ'] = self.extraer_numerodoc_MRZ(lineas_raw[0])
            self.mrz['datosMRZ']['fechaNacimiento_MRZ']=lineas_raw[1][:6]
            self.mrz['datosMRZ']['fechaVencimiento_MRZ']=lineas_raw[1][8:14]
            apellido_nombre_mrz=self.procesar_linea_MRZ(lineas_raw[2])
            self.mrz['datosMRZ']['apellidos_MRZ'] = apellido_nombre_mrz[0]+' '+apellido_nombre_mrz[1]
            self.mrz['datosMRZ']['nombres_MRZ'] = apellido_nombre_mrz[2]+' '+apellido_nombre_mrz[3]
            self.mrz['datosMRZ']['nacionalidad_MRZ'] = self.extraer_abreviatura_pais(lineas_raw[1])
            self.set_obtener_sexo_mrz()
            
            #OBTENER EL RUT DE LINEA
            self.mrz['datosMRZ']['RUN_MRZ'] = self.extraer_run_mrz(lineas_raw[1])
        # Si se proporciona keys_to_update, solo se actualizan esas claves.
        if keys_to_update is not None:
            data = {key: data[key] for key in keys_to_update if key in data}
        
        # Actualiza las demás claves proporcionadas en data
        for key, value in data.items():
            if hasattr(self, key) and key not in claves_mrz:  # Ignora las claves MRZ ya que ya se han procesado
                setattr(self, key, value)
        
        self.fecha_nacimiento=self.transformar_fecha_front(self.fecha_nacimiento)
        self.fecha_vencimiento=self.transformar_fecha_front(self.fecha_vencimiento)
        self.fecha_emision=self.transformar_fecha_front(self.fecha_emision)
        self.transformar_nombre_pais()
        hola=ocr.limpiar_datos(self.sexo,'sexo')
        print(hola)
                

    def actualizar_datos_mrz(self, datos_actualizacion):
        for clave, valor in datos_actualizacion.items():
            if clave in self.mrz["datosMRZ"]:
                self.mrz["datosMRZ"][clave] = valor
        self.mrz["tieneMRZ"] = True
    

    

    def extraer_numerodoc_MRZ(self, linea_raw0):
        # Extraer todos los dígitos de la cadena
        digitos = re.findall('\d', linea_raw0)

        # Unir los dígitos en una sola cadena y obtener los primeros 9
        return ''.join(digitos)[:9]


    def set_obtener_sexo_mrz(self):
        linea2MRZ=self.mrz["datosMRZ"]["textoGeneral_MRZ"].split()[1]
        sexo_salida=''
        if (len(linea2MRZ)==28):
            sexo = linea2MRZ[7:8]
            sexo_salida = sexo
        self.mrz["datosMRZ"]["sexo_MRZ"]=sexo_salida
    

    def obtener_nacionalidad_mrz(self): 
        #se quiere modificar la nacionalidad del diccionarioMRZ
        nacionalidad=''
        linea1MRZ=self.mrz["datosMRZ"]["textoGeneral_MRZ"].split()[0]

        if (len(linea1MRZ)==18):
            tmp = linea1MRZ[2:5]
            nacionalidad = tmp

        self.mrz["datosMRZ"]["nacionalidad_MRZ"]= nacionalidad
    


    def procesar_linea_MRZ(self,input_string):
        # Dividir el string en partes usando '<' como separador
        partes = input_string.split('<')
        
        # Eliminar strings vacíos
        partes = [parte for parte in partes if parte]
        
        # Eliminar cualquier carácter que no esté en el rango a-z y A-Z
        partes = [re.sub('[^a-zA-Z]', '', parte) for parte in partes]
        
        return partes
  

    def extraer_run_mrz(self, mrz_raw_1):
        # Buscar los patrones en la cadena
        chl_match = re.search('[A-Z]{3}(\d{8})', mrz_raw_1)
        k_match = re.search('<(\w)', mrz_raw_1)

        # Extraer los caracteres
        chl_chars = chl_match.group(1) if chl_match else ''
        k_char = k_match.group(1) if k_match else ''

        # Combinar los caracteres
        result = (chl_chars + k_char)

        return result

    def extraer_abreviatura_pais(self, cadena):
        # Buscar el patrón en la cadena
        pais_match = re.search('[A-Z]{3}', cadena)

        # Extraer los caracteres
        pais_chars = pais_match.group(0) if pais_match else ''

        return pais_chars
    def transformar_fecha_front(self,fecha): #check

        meses_abreviados = {
        "ENER": "01",
        "FEBR": "02",
        "MAR": "03",
        "ABR": "04",
        "MAYO": "05",
        "JUN": "06",
        "JUL": "07",
        "AGO": "08",
        "SEPT": "09",
        "OCT": "10",
        "NOV": "11",
        "DIC": "12"
    }
        fecha_formato=''
        if (len(fecha) == 9):
            dia = fecha[0:2]
            mes = fecha[2:5]
            #condicionar mes para pasarlo al numero
            if mes in meses_abreviados:
                valor_numerico = meses_abreviados[mes]
            else:
                return fecha_formato
            año = fecha[7:]
            fecha_formato= año+valor_numerico+dia
            return fecha_formato
        elif (len(fecha) == 10):
            dia = fecha[0:2]
            mes = fecha[2:6]
            #condicionar mes para pasarlo al numero
            if mes in meses_abreviados:
                valor_numerico = meses_abreviados[mes]
            else:
                return fecha_formato
            año = fecha[8:]
            fecha_formato= año+valor_numerico+dia
            return fecha_formato
        else:
            return fecha_formato #si la fecha no tiene esos tamaños 

    def transformar_nombre_pais(self):
        trat_nacional = tools.cargar_trat_nacionalidades()

        # Comprobar si dic_paises es un diccionario
        if not isinstance(trat_nacional, dict):
            raise ValueError("dic_paises debe ser un diccionario.")

        # Comprobar si dic_paises es None
        if trat_nacional is None:
            raise ValueError("dic_paises no puede ser None.")
        #QUE SUSCEDE SI NO EXISTE LA CLAVE???. CONTROLAR ESO..


        if  self.nacionalidad!='' and self.nacionalidad in trat_nacional:
            abreviatura=trat_nacional[self.nacionalidad]
            self.nacionalidad = abreviatura



"""declarar una funcion que realize validaciones de los datos de la cedula
def validar_datos(self): la funcion me retorna un diccionari con una estructura que muestte los datos 
necesarios para saber si los campos coinciden..."""