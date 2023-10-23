from flask import Flask, jsonify
from carnet import carnet 
import cv2
import sys
from PIL import Image
from pylab import * 
import numpy as np
import pytesseract
from google.cloud import vision
from google.cloud.vision_v1 import types
import argparse
import os
import re

#cedula derecha

#image = array(Image.open('app/cedula.jpg'))
pytesseract.pytesseract.tesseract_cmd =r'c:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def OCR(imagen):
    texto = pytesseract.image_to_string(imagen)
    return str(texto)


image= cv2.imread('app/image/a2.jpg')#imagen frontal
image2= cv2.imread('app/image/24.2.jpg')#imagen reverso

title('Cedula de Indentidad')

#escala gray imagen frontal
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


#foto back
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




#recorte de imagenes a obtener lectura 
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
nacio_en= rut_bin2[211:247 , 182:600] #check pero con detalles
profesion = rut_bin2[242:274,182:403] #check
mrz = rut_otsu2[354:492, 42:800] #check
nombre_mrz= rut_otsu2[440:482, 418:800] #check
apellido_mrz=rut_otsu2[440:478, 44:375] #check
rut_mrz = rut_otsu2[395:440,495:747] #check
documento_mrz=rut_bin2[354:398,170:400] #check

#para mejor vision del mrz
#gray3 = cv2.medianBlur(mrz, 5)
#dst2 = cv2.adaptiveThreshold(gray3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)



#plt.imshow(rut_mrz,cmap='gray')

#show()

#edges = cv2.Canny(mrz, 100, 200)

#img_float = np.float32(mrz)/255.0
#img_log = cv2.log(img_float)
#gamma = 0.2
#c = 1
#img_filtered = np.exp(c * img_log) ** gamma
#img_filtered = np.uint8(img_filtered * 255)

#sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
#sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
#img = cv2.GaussianBlur(image, (3, 3), sigmaX=0, sigmaY=0)


#data String Frontal
#hacer esto a cada uno de los campos reemplaza y quita los espacios
data_nombre= OCR(nombre_texto).replace(' ', '').split(' ') 
data_apellido= OCR(apellido_texto).replace('\n', '').strip().split(' ')
data_fecha_nacimiento= OCR(fecha_nacimiento).replace('<', '').replace('>', '').split(' ') #buscar una forma de quitar todos los caracteres
data_rut_grande= OCR(rut_grande).replace('\n', '').replace('.', '').replace('-', '').split(' ')
data_nacionalidad= OCR(nacionalidad).split(' ')
data_fecha_emision= OCR(fecha_emision).split(' ')
data_fechaV_texto= OCR(fechaV_texto).split(' ')
data_documento=OCR(doc_texto).replace('.', '').replace('\n', '').split(' ')

#data String Back
data_nombre_back=OCR(nombre_mrz).replace(" ", '').replace('<', '').split()
data_apellido_back=OCR(apellido_mrz).replace(" ", '').replace('<', '').split()
data_rut_mrz = OCR(rut_mrz).replace('<', '').split()
data_documento_mrz=OCR(documento_mrz).replace(" ", '').replace('<', '').split()

porcentaje_de_aprobar= 0.8  #si la comparación de datos supera este umbral es porque es el nombre

#crear una sola funcion de calcular luego
##calcular el porcentaje de parecerse el nombre
calcular = 0
contar = 0
for i in range(len(data_nombre_back[0])):
    datos1=data_nombre[0]
    datos2=data_nombre_back[0]
    if(datos1[i]==datos2[i]):
        contar = contar + 1   
    calcular = contar/len(data_nombre[0])

if (calcular >=porcentaje_de_aprobar):
    print("El nombre se asemeja")

else:
    print("El nombre NO se asemeja")

#calcular el porcentaje de parecerse el apellido
calcular2 = 0
contar2 = 0
for j in range(len(data_apellido_back[0])):
    datos3=data_apellido[0]
    datos4=data_apellido_back[0]
    if(datos3[j] == (datos4[j])):
        contar2 = contar2+1
    calcular2 = contar2/len(data_apellido[0])

if (calcular2 >=porcentaje_de_aprobar):
    print("El apellido se asemeja")  
else:
    print("El apellido NO se asemeja")


#calcular el porcentaje de parecerse el documento
calcular3 = 0
contar3 = 0
for j in range(len(data_documento_mrz[0])):
    datos5=data_documento[0]
    datos6=data_documento_mrz[0]
    if(datos3[j] == (datos4[j])):
        contar3 = contar3+1
    calcular3 = contar3/len(data_documento[0])

if (calcular3 >=porcentaje_de_aprobar):
    print("El documento es el mismo")  
else:
    print("El apellido NO se asemeja")


#calcular el porcentaje de parecerse el rut
calcular4 = 0
contar4 = 0
for j in range(len(data_rut_mrz[0])):
    datos7=data_rut_grande[0]
    datos8=data_rut_mrz[0]
    if(datos7[j] == (datos8[j])):
        contar4 = contar4+1
    calcular4 = contar4/len(data_documento[0])

if (calcular4 >=porcentaje_de_aprobar):
    print("El RUT es el mismo")  
else:
    print("El RUT NO se asemeja")

