from flask import Flask, jsonify
from carnet import carnet 
import cv2
from PIL import Image
from pylab import * 
import numpy as np
import pytesseract

image= cv2.imread('app/image/a2.jpg')#imagen frontal
image2= cv2.imread('app/image/24.2.jpg')#imagen reverso

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
#rut_chico=rut_otsu[282:308,686:808] #rut en foto pequeña falta mejorar su visibilidad

#lectura trasera
nacio_en= rut_bin[211:247 , 182:600] 
profesion = rut_bin[242:274,182:403]
mrz = rut_otsu[354:492, 42:800]
nombre_mrz= rut_otsu[440:482, 418:800]
apellido_mrz=rut_otsu[440:482, 418:800]
rut_mrz = rut_otsu[44:84,453:705]
documento_mrz=rut_otsu[88:127,4:330]

gray2 = cv2.medianBlur(mrz, 5)
dst2 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

plt.imshow(mrz,cmap='gray')
show()

print("MRZ: " , OCR(mrz))

def limpiar_datos(ocr_result):
    cleaned_data = ocr_result.replace(' ', '').replace('<', '').replace('>', '').replace('.', '').replace('-', '').split()
    return cleaned_data

def comparar_datos(datos_frontales, datos_traseros, umbral):
    # Comparación de nombres
    porcentaje_de_aprobar = umbral
    calcular = 0
    contar = 0
    for i in range(len(datos_frontales[0])):
        datos1 = datos_frontales[0]
        datos2 = datos_traseros[0]
        if datos1[i] == datos2[i]:
            contar = contar + 1
        calcular = contar / len(datos_frontales[0])

    if calcular >= porcentaje_de_aprobar:
        return True
    else:
        return False
    
 #data string front
data_nombre = limpiar_datos(OCR(nombre_texto))
data_apellido = limpiar_datos(OCR(apellido_texto))
data_fecha_nacimiento = limpiar_datos(OCR(fecha_nacimiento))
data_rut_grande = limpiar_datos(OCR(rut_grande))
data_nacionalidad = OCR(nacionalidad).split() #limpiar?
data_fecha_emision = OCR(fecha_emision).split()  #limpiar?
data_fechaV_texto = OCR(fechaV_texto).split() #limpiar?

# data String Back
data_nombre_back = limpiar_datos(OCR(nombre_mrz))
data_apellido_back = limpiar_datos(OCR(apellido_mrz))
data_rut_back = limpiar_datos(OCR(rut_mrz))

porcentaje_de_aprobar= 0.8  

nombres_comparacion = comparar_datos(data_nombre_back,data_nombre,porcentaje_de_aprobar)
apellido_comparacion = comparar_datos(data_apellido_back,data_apellido,porcentaje_de_aprobar)
rut_comparacion = comparar_datos(data_rut_back, data_rut_grande,porcentaje_de_aprobar)