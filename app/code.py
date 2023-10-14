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
    texto = pytesseract.image_to_string(imagen)
    return texto

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

 # Binarización
ret,rut_bin = cv2.threshold(rut_eq,120,255,cv2.THRESH_BINARY)

# Binarización otsu
ret2,rut_otsu = cv2.threshold(rut_eq, 127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)   


doc_texto = rut_bin[275:310, 487:663] #numero documento check
fechaV_texto = rut_bin[335:367 , 477:667] #fecha vencimiento check
nombre_texto = rut_bin[171:211 , 291:826] #nombre check
apellido_texto = rut_bin[89:152 , 292:658] #apellido check
rut_chico=rut_eq[282:310,690:808] #rut en foto pequeña check
rut_grande= rut_bin[460:496 , 98:273] #rut grande check
nacionalidad= rut_bin[220:265, 291:425] #nacionalidad check
#aplicar que las imagenes se vean mejor investigar

plt.imshow(rut_chico,cmap='gray')
show()

#Probar Tesseract 
print("numero de documento: " , OCR(rut_grande))
print("numero de documento: " , OCR(rut_chico))

