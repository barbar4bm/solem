from flask import Flask, jsonify
import cv2
from PIL import Image
from pylab import * 
import numpy as np
import pytesseract
import time

inicio = time.time()
image= cv2.imread('app/image/a2.jpg')#imagen frontal
image2= cv2.imread('app/image/24.2.jpg')#imagen reverso

#si se usa windows , esto es necesario
#pytesseract.pytesseract.tesseract_cmd =r'c:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def OCR(imagen):
    texto = pytesseract.image_to_string(imagen)
    return str(texto)

title('Cedula de Indentidad')
    
#filtros iamgen delantera
# Cambio de espacio de color de BGR a RGB
img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Cambio de espacio de color BGR a GRAY
gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# Ecualización
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
rut_eq = clahe.apply(gray)
equ = cv2.equalizeHist(rut_eq)
 # Binarización
ret,rut_bin = cv2.threshold(rut_eq,100,255,cv2.THRESH_BINARY)
# Binarización otsu
ret2,rut_otsu = cv2.threshold(rut_eq,127,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   

#filtro foto back
# Cambio de espacio de color de BGR a RGB
img_rgb2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
# Cambio de espacio de color BGR a GRAY
gray2 = cv2.cvtColor(img_rgb2, cv2.COLOR_BGR2GRAY)
# Ecualización
clahe2 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
rut_eq2 = clahe2.apply(gray2)
equ2 = cv2.equalizeHist(rut_eq2)
 # Binarización
ret,rut_bin2 = cv2.threshold(rut_eq2,100,255,cv2.THRESH_BINARY)
# Binarización otsu
ret2,rut_otsu2 = cv2.threshold(rut_eq2,127,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   

#lectura delantera
nombre_texto = rut_bin[171:211 , 291:806] #nombre check
apellido_texto = rut_bin[88:152 , 292:520] #apellido check
rut_grande = rut_bin[460:496 , 98:273] #rut grande check
nacionalidad = rut_bin[220:265, 291:425] #nacionalidad check
sexo = rut_bin[229:257, 486:509] #no detecta solo un caracter
fecha_nacimiento = rut_bin[276:311 , 250:480] #fecha nacimiento check
doc_texto = rut_bin[275:310, 487:663] #numero documento check
fecha_emision = rut_bin[330:369 , 292:463] #fecha emision check
fechaV_texto = rut_bin[328:370 , 473:670] #fecha vencimiento check 
plt.imshow(sexo,cmap='gray')
show()
print(OCR(sexo))

#rut_chico=rut_otsu[282:308,686:808] #rut en foto pequeña falta mejorar su visibilidad

#lectura trasera
nacio_en = rut_bin2[211:247 , 182:600] 
profesion = rut_bin2[242:274,182:403]
mrz = rut_otsu2[354:492, 42:800]
nacionalidad_doc_mrz = rut_otsu2[343:398, 37:800]
fechas_rut_mrz =rut_otsu2[390:436,37:800]
nombre_full_mrz = rut_otsu2[432:482,37:800]

print("la cantidad de elementos de primera linea es: ",len(OCR(nombre_full_mrz)))
#plt.imshow(nacionalidad_doc_mrz,cmap='gray')
#show()



def limpiar_datos(ocr_result):
    cleaned_data = str(ocr_result).replace('\n', '').replace(' ', '').replace('<', '').replace('>', '').replace('.', '').replace('-', '').replace(',', '').replace(')', '').replace('(', '').split()
    return cleaned_data

paises_abreviados = {
    "ALEMANA" : "AL",
    "CHILENA": "CHL",
    "BOL": "BOL",
    "PERUANA": "PE",
    "ARGENTINA" : "AR",
    "COLOMBIANA" : "COL",
    "VENEZOLANA": "VEN",
    "HAITIANA": "HAI",
}
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

 #data string front
data_nombre = limpiar_datos(OCR(nombre_texto))
data_apellido = limpiar_datos(OCR(apellido_texto))
data_fecha_nacimiento = limpiar_datos(OCR(fecha_nacimiento))
data_rut_grande = limpiar_datos(OCR(rut_grande))
data_nacionalidad = limpiar_datos(OCR(nacionalidad))
data_fecha_emision = limpiar_datos(OCR(fecha_emision))  
data_fechaV_texto = limpiar_datos(OCR(fechaV_texto)) 
data_numero_doc = limpiar_datos(OCR(doc_texto))

# data String Back
data_nacionalidad_doc_mrz = limpiar_datos(OCR(nacionalidad_doc_mrz))
data_fechas_rut_mrz = limpiar_datos(OCR(fechas_rut_mrz))
data_nombre_full_mrz = limpiar_datos(OCR(nombre_full_mrz))
#union y/o separacion de datos 
data_apellido_nombre = data_apellido[0] + data_nombre[0]

#funciones para cada caso
def comparar_nombre_completo(nombre , arreglo, umbral):
    porcentaje_de_aprobar = umbral
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

def comparar_nacionalidad(nacionalidad_front,nacionalidad_back,umbral):
    porcentaje_de_aprobar = umbral
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
def transformar_fecha_front(fecha): #check
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

def transformar_pais_a_abreviatura(pais, paises_abreviados):

    if pais in paises_abreviados:
        return paises_abreviados[pais]
    else:
        return "No se encontró la abreviatura para el país especificado."




def obtener_nacionalidad_mrz(data): 
    fecha_salida=''
    if (len(data)==18):
        fecha = data[2:5]
        fecha_salida = fecha
        return fecha_salida
    else:
        return fecha_salida
def obtener_fecha_vencimiento_mrz(data): #check
    fecha_salida=''
    if (len(data)==28):
        fecha = data[8:14]
        fecha_salida = fecha
        return fecha_salida
    else:
        return fecha_salida

def obtener_fecha_nacimiento_mrz(data): #check
    fecha_salida=''
    if (len(data)==28):
        fecha = data[0:6]
        fecha_salida = fecha
        return fecha_salida
    else:
        return fecha_salida
    
def obtener_documento_mrz(data): 
    documento_salida=''
    if (len(data)==18):
        documento = data[5:14]
        documento_salida = documento
        return documento_salida
    else:
        return documento_salida

def comparar_documentos(front,back,umbral): 
    porcentaje_de_aprobar=umbral
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



#umbral de aprobacion
porcentaje_de_aprobar= 0.85 
 
#Verificaciones
abreviatura = transformar_pais_a_abreviatura(data_nacionalidad[0], paises_abreviados)
print(f"La abreviatura para {data_nacionalidad[0]} es: {abreviatura}")
obtener = obtener_nacionalidad_mrz(data_nacionalidad_doc_mrz[0])
comparar_nacionalidad = comparar_nacionalidad(abreviatura,obtener,porcentaje_de_aprobar)
print("nacionalidad iguales?",comparar_nacionalidad)
print(obtener,"a" , abreviatura)
compara_nombre = comparar_nombre_completo(data_apellido_nombre,data_nombre_full_mrz,porcentaje_de_aprobar)
print('Nombres iguales?',compara_nombre)
compara_fecha_vencimiento = comparar_fecha(transformar_fecha_front(data_fechaV_texto[0]),obtener_fecha_vencimiento_mrz(data_fechas_rut_mrz[0]),porcentaje_de_aprobar)
print('Fecha de vencimiento iguales?',compara_fecha_vencimiento)
compara_fecha_nacimiento = comparar_fecha(transformar_fecha_front(data_fecha_nacimiento[0]),obtener_fecha_nacimiento_mrz(data_fechas_rut_mrz[0]),porcentaje_de_aprobar)
print('Fecha de nacimiento iguales?',compara_fecha_nacimiento)
compara_documento= comparar_documentos(data_numero_doc[0],obtener_documento_mrz(data_nacionalidad_doc_mrz[0]),porcentaje_de_aprobar)
print('Número de documento iguales?',compara_documento)

fin = time.time()
print("El tiempo de ejecución final fue: ", fin-inicio)