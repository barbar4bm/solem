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
import

#image = array(Image.open('app/cedula.jpg'))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
image= cv2.imread('app/cedula.jpg')
title('Cedula de Indentidad')

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

#Comparar
foto_grande = rut_otsu[90:275, 30:175]
foto_pequeña = rut_otsu[140:200, 440:510]
plt.imshow(foto_pequeña,cmap='gray')
show()

#aplicar tesseract para obtener informacion 
# Establece la variable de entorno con la ruta de tu archivo .json (mala practica)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/ocrtry-401614-37f6a7cca750.json"

# Inicializa el cliente de Vision
client = vision.ImageAnnotatorClient()

# Abre la imagen desde un archivo
with open('app/cedula.jpg', 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Usa el OCR de Google Vision
response = client.text_detection(image=image)
texts = response.text_annotations

# Imprime el texto detectado
for text in texts:
    print('\n"{}"'.format(text.description))

#Probar Tesseract 
