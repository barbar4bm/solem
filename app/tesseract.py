from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2      

pytesseract.pytesseract.tesseract_cmd =r'c:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
imagen_color = cv2.imread('app/cedula.jpg')
#imagen_rgb = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2RGB)
imagen_gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)
#clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#rut_eq = clahe.apply(imagen_gris)
# Binarización
#ret,rut_bin = cv2.threshold(rut_eq,127,255,cv2.THRESH_BINARY)
#ret2,rut_otsu = cv2.threshold(rut_eq, 127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

image= pytesseract.image_to_string(imagen_gris)
print(image)

