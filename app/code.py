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

image= cv2.imread('app/image/a7.jpg')

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
ret,rut_bin = cv2.threshold(rut_eq,127,255,cv2.THRESH_BINARY)

# Binarización otsu
ret2,rut_otsu = cv2.threshold(rut_eq, 127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)   



doc_texto = rut_bin[275:310, 487:663] #numero documento check
fechaV_texto = rut_bin[335:367 , 477:667] #fecha vencimiento check
nombre_texto = rut_bin[171:211 , 291:826] #nombre check
apellido_texto = rut_bin[89:152 , 292:658] #apellido check
rut_chico=rut_eq[287:310,690:809]


plt.imshow(rut_chico,cmap='gray')
show()

#Probar Tesseract 
print("numero de documento: " , OCR(rut_chico))
#print("fecha de vencimiento: " , OCR(fechaV_texto))