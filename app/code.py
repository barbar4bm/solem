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

image= cv2.imread('app/cedula.jpg')
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

cv2.rectangle(rut_otsu, (30, 90), (175, 275), (0,0,255), 4) #foto grande
cv2.rectangle(rut_otsu, (440, 140), (510, 200), (0,0,255), 4) #foto pequeña
cv2.rectangle(rut_otsu, (312, 170), (425, 200), (0,0,255), 4)

#Comparar
foto_grande = rut_otsu[90:275, 30:175]
foto_pequeña = rut_otsu[140:200, 440:510]
doc = rut_bin[170:200, 312:423]
plt.imshow(doc,cmap='gray')
show()

#Probar Tesseract 
print(OCR(doc))