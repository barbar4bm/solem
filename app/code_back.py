from flask import Flask, jsonify
from carnet import carnet 
import cv2
from PIL import Image
from pylab import * 
import numpy as np
import pytesseract


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

image= cv2.imread('app/image/24.3.jpg')

title('Cedula de Indentidad')


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

#lectura trasera
nacio_en= rut_bin[211:247 , 182:600] #check pero con detalles
profesion = rut_bin[242:274,182:403]
mrz = rut_otsu[354:492, 42:800]

gray2 = cv2.medianBlur(mrz, 5)
dst2 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

plt.imshow(nacio_en,cmap='gray')
show()
plt.imshow(profesion,cmap='gray')
show()
plt.imshow(mrz,cmap='gray')
show()

print("Nacio en: " , OCR(nacio_en))
print("Profesión: " , OCR(profesion))
print("MRZ: " , OCR(mrz))


