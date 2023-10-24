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
#sexo = rut_otsu[222:263, 450:600] #no detecta genero
fecha_nacimiento = rut_bin[276:311 , 250:480] #fecha nacimiento check
doc_texto = rut_bin[275:310, 487:663] #numero documento check
fecha_emision = rut_bin[330:369 , 292:463] #fecha emision check
fechaV_texto = rut_bin[335:367 , 477:667] #fecha vencimiento check 
fecha_anio_ven_del = rut_bin[335:367 , 477:667]
#plt.imshow(rut_bin,cmap='gray')
#show()
#rut_chico=rut_otsu[282:308,686:808] #rut en foto pequeña falta mejorar su visibilidad

#lectura trasera
nacio_en = rut_bin2[211:247 , 182:600] 
profesion = rut_bin2[242:274,182:403]
mrz = rut_otsu2[354:492, 42:800]
nombre_mrz = rut_otsu2[440:482, 418:800]
apellido_mrz = rut_otsu2[440:478, 44:375]
rut_mrz = rut_otsu2[395:440,495:747]
documento_mrz=rut_otsu2[355:400,170:400]
nacionalidad_mrz = rut_otsu2[400:435,420:495]
fecha_anio_venci = rut_otsu2[395:431,244:297]#check
fecha_mes_venci = rut_otsu2[395:431,295:345]#check
#fecha_dia_venci_seg = rut_otsu2[396:436,360:392]#lee el 5 en a1
#fecha_dia_venci_pri = rut_otsu2[395:437,347:370] # no lee el 1 
fecha_dia_venci = rut_otsu2[394:435,347:394] #no lee día
plt.imshow(rut_otsu2,cmap='gray')
show()
plt.imshow(fecha_dia_venci,cmap='gray')
show()
print(OCR(fecha_dia_venci))


def limpiar_datos(ocr_result):
    cleaned_data = str(ocr_result).replace('\n', '').replace(' ', '').replace('<', '').replace('>', '').replace('.', '').replace('-', '').split()
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

#nacionalidad en diccionario? 
#nacionalidad_diccionario = obtener_nombre_pais_diccionario(nacionalidad,paises_abreviados)
#print(nacionalidad_diccionario)
# data String Back
data_nombre_back = limpiar_datos(OCR(nombre_mrz))
data_apellido_back = limpiar_datos(OCR(apellido_mrz))
data_rut_back = limpiar_datos(OCR(rut_mrz))
data_numero_doc_back = limpiar_datos(OCR(documento_mrz))
data_nacionalidad_back = limpiar_datos(OCR(nacionalidad_mrz))

#umbral de aprobacion
porcentaje_de_aprobar= 0.8 
 
#Verificaciones
nombres_comparacion = comparar_datos(data_nombre,data_nombre_back,porcentaje_de_aprobar)
print("Verificación de nombres: ",nombres_comparacion)
apellido_comparacion = comparar_datos(data_apellido,data_apellido_back,porcentaje_de_aprobar)
print("Verificación de apellidos: ",apellido_comparacion)
rut_comparacion = comparar_datos(data_rut_grande, data_rut_back,porcentaje_de_aprobar)
print("Verificación de rut: ",rut_comparacion)
#nacionalidad_comparacion = comparar_datos(nacionalidad_diccionario,data_nacionalidad_back,porcentaje_de_aprobar)
#print(nacionalidad_comparacion)
#fecha_dia_comparacion = comparar_datos() 
#print("verificacion de fecha: ")
numero_docu_comparacion = comparar_datos(data_numero_doc,data_numero_doc_back,porcentaje_de_aprobar)
print("Verificación de número de documento: ", numero_docu_comparacion)
fin = time.time()
print("El tiempo de ejecución final fue: ", fin-inicio)