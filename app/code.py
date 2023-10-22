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

#cedula derecha

#image = array(Image.open('app/cedula.jpg'))
pytesseract.pytesseract.tesseract_cmd =r'c:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def OCR(imagen):
    texto = pytesseract.image_to_string(imagen,lang='spa')
    return str(texto)

def rut_comparacion(foto1, foto2):
    # Calcula el histograma de las imágenes
    hist1 = cv2.calcHist([foto1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([foto2], [0], None, [256], [0, 256])
    
    # Calcula la correlación entre los histogramas
    correlacion = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    # Si la correlación es mayor que un umbral, las imágenes son consideradas iguales
    umbral = 0.95  # Puedes ajustar este umbral según tus necesidades
    if correlacion > umbral:
        return True
    else:
        return False

image= cv2.imread('app/image/a1.jpg')


title('Cedula de Indentidad')
#escala gray

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
nacio_en= rut_bin[211:247 , 182:600] #check pero con detalles
profesion = rut_bin[242:274,182:403]
mrz = rut_otsu[354:492, 42:800]

gray2 = cv2.medianBlur(mrz, 5)
dst2 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)



plt.imshow(nombre_texto,cmap='gray')
show()

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
data_nombre= OCR(nombre_texto).split(' ') #hacer esto a cada uno de los campos

print("numero de documento: " , len(data_nombre))
print("numero de documento: " , OCR(nacionalidad))
print("numero de documento: " , OCR(fecha_nacimiento))
#print("numero de documento: " , OCR(rut_chico))

for i in range(len(data_nombre)):
    print(data_nombre[i]) 