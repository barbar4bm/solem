from flask import Flask, jsonify
from carnet import carnet 
import cv2
import sys
from PIL import Image
from pylab import * 
import numpy as np
import pytesseract

#cedula derecha

image = array(Image.open('app/cedula.jpg'))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
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
cv2.rectangle(rut_otsu , (130, 15), (180, 45), (0,0,255), 4) #bandera chile
cv2.rectangle(rut_otsu, (305, 170), (430, 210), (0,0,255), 4) #documento


plt.imshow(rut_otsu, cmap='gray')
show()
#aplicar OCR
