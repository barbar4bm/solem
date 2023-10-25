from flask import Flask, jsonify
from carnet import carnet 
import cv2
from PIL import Image
from pylab import * 
import numpy as np
import pytesseract
import time

inicio = time.time()
image= cv2.imread('app/image/a1.jpg')#imagen frontal
image2= cv2.imread('app/image/16.2.jpeg')#imagen reverso

#si se usa windows , esto es necesario
pytesseract.pytesseract.tesseract_cmd =r'c:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

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
#sexo = rut_otsu[222:263, 450:600] #no detecta genero
fecha_nacimiento = rut_bin[276:311 , 250:480] #fecha nacimiento check
doc_texto = rut_bin[275:310, 487:663] #numero documento check
fecha_emision = rut_bin[330:369 , 292:463] #fecha emision check
fechaV_texto = rut_bin[328:370 , 473:670] #fecha vencimiento check 

#plt.imshow(fechaV_texto,cmap='gray')
#show()


#rut_chico=rut_otsu[282:308,686:808] #rut en foto pequeña falta mejorar su visibilidad

#lectura trasera
nacio_en = rut_bin2[211:247 , 182:600] 
profesion = rut_bin2[242:274,182:403]
mrz = rut_otsu2[354:492, 42:800]
nacionalidad_rut_mrz = rut_otsu2[343:395, 37:800]
fechas_rut_mrz =rut_otsu2[390:436,37:800]
nombre_full_mrz = rut_otsu2[432:482,37:800]

#plt.imshow(fecha_mes_venci,cmap='gray')
#show()

def limpiar_datos(ocr_result):
    cleaned_data = str(ocr_result).replace('\n', '').replace(' ', '').replace('<', '').replace('>', '').replace('.', '').replace('-', '').replace(',', '').replace(')', '').replace('(', '').split()
    return cleaned_data

def comparar_datos(datos_frontales, datos_traseros, umbral):
    # Comparación de nombres
    porcentaje_de_aprobar = umbral
    calcular = 0
    contar = 0
    for i in range(len(datos_traseros[0])):
        datos1 = datos_frontales[0]
        datos2 = datos_traseros[0]
        if (datos1[i] == datos2[i]):
            contar = contar + 1
        calcular = contar / len(datos_frontales[0])

    if (calcular >= porcentaje_de_aprobar):
        return True
    else:
        return False

def obtener_nombre_pais_diccionario(abreviatura, paises_abreviados):
    if abreviatura in paises_abreviados:
        return abreviatura
    else:
        return None
    
paises_abreviados = {
    "ALEMANA" : "AL",
    "CHILENA": "CHL",
    "BOL": "BOL",
    "PERUANA": "PE",
    "ARGENTINA" : "AR",
    "COLOMBIANA" : "COL",
    "VENEZOLANA": "VEN",
    "HAITIANA": "HAI",

     #Agrega más pares clave-valor según sea necesario
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

#union y/o separacion de datos 
data_apellido_nombre = data_apellido[0] + data_nombre[0]

def transformar_fecha_front(fecha): #check
    fecha_formato=''
    if (len(fecha) == 9):
        dia = fecha[0:2]
        mes = fecha[2:5]
        #condicionar mes para pasarlo al numero
        año = fecha[7:]
        fecha_formato= año+mes+dia
        return fecha_formato
    elif (len(fecha) == 10):
        dia = fecha[0:2]
        mes = fecha[2:6]
        #condicionar mes para pasarlo al numero
        año = fecha[8:]
        fecha_formato= año+mes+dia
        return fecha_formato
    else:
        return fecha_formato #si la fecha no tiene esos tamaños 


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

#nacionalidad en diccionario? 
#nacionalidad_diccionario = obtener_nombre_pais_diccionario(nacionalidad,paises_abreviados)
#print(nacionalidad_diccionario)
# data String Back
data_nacionalidad_rut_mrz = limpiar_datos(OCR(nacionalidad_rut_mrz))
data_fechas_rut_mrz = limpiar_datos(OCR(fechas_rut_mrz))
data_nombre_full_mrz = limpiar_datos(OCR(nombre_full_mrz))


#umbral de aprobacion
porcentaje_de_aprobar= 0.8 
 
#Verificaciones
#nombres_comparacion = comparar_datos(data_apellido_nombre,data_nombre_full_mrz,porcentaje_de_aprobar)
#print("Verificación de nombres: ",nombres_comparacion)
#apellido_comparacion = comparar_datos(data_apellido,data_apellido_back,porcentaje_de_aprobar)
#print("Verificación de apellidos: ",apellido_comparacion)
#rut_comparacion = comparar_datos(data_rut_grande, data_rut_back,porcentaje_de_aprobar)
#print("Verificación de rut: ",rut_comparacion)
#nacionalidad_comparacion = comparar_datos(nacionalidad_diccionario,data_nacionalidad_back,porcentaje_de_aprobar)
#print(nacionalidad_comparacion)
#fecha_dia_comparacion = comparar_datos() 
#print("verificacion de fecha: ")
#numero_docu_comparacion = comparar_datos(data_numero_doc,data_numero_doc_back,porcentaje_de_aprobar)
#print("Verificación de número de documento: ", numero_docu_comparacion)
fin = time.time()
print("El tiempo de ejecución final fue: ", fin-inicio)