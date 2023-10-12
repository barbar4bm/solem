from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2      
from matplotlib import pyplot as plt
from pytesseract import Output
import re


#paso 1: Pre procesamiento de imaágenes (acceder a la imagen)
path_Example = ’delantera.jpg’
img_color = cv2.imread(path_Example)
plt.imshow(img_color)
plt.show()

#paso 2: Transformar imagen a escala de grises 
img_gris = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
plt.imshow(img_gris)
plt.show()

#paso 3: Binarización de la imagen (blanco y negro)
thresh_img = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
plt.imshow(thresh_img)
plt.show()

#paso 4: operacion morfologica (eliminar ruido y suavizar letras)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
opening_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel,iterations=1)
plt.imshow(opening_image)
plt.show()

#paso 5: invertir imagen (fondo blanco)
invert_image = 255 - opening
plt.imshow(invert_image)
plt.show()

#paso 6: elección del idioma en tesseract
def ocr(image):
    custom_config = r'-l spa - psm 11'
    text = pytesseract.image_to_string(image,config=custom_config )
    return text


#paso 7: dibujando las cajas o rectangulos
data_image= pytesseract.image_to_data(invert, output_type=Output.DICT)

#paso 8: dibujando cajas donde detecta texto
n_boxes = len(data_image['text'])
for i in range(n_boxes):
  if int(data_image['conf'][i]) > 50:
    (x, y, w, h) = (data_image['left'][i], data_image['top'][i],data_image['width'][i], data_image['height'][i])
     img = cv2.rectangle(img_color, (x, y),(x + w, y + h),(255,0,0), 2)
plt.imshow(img)
plt.show()
cv2.imwrite('ImagenRectangulos.jpg',img)


#paso 9: dibujando cajas solo en las fechas

n_boxes = len(data_image['text'])
for i in range(n_boxes):
    if int(data_image['conf'][i]) > 40:
       match= re.match('\w{2}-\w{2}-\w{4}',data_image['text'][i])
    if match:
      (x, y, w, h) = (data_image['left'][i], data_image['top'][i],data_image['width'][i], data_image['height'][i])
      img = cv2.rectangle(img_color, (x, y), (x + w, y + h), (255,0,0),2)
plt.imshow(img)
plt.show()

#paso 10:  extracción de caracteres
def main_process(path):
    img_color=cv2.imread(path) 
    img_gris=cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) 
    thresh = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2)) 
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel,iterations=1) 
    invert = 255 - opening
    text=ocr(invert)
    frontal=re.findall('\w{2}-\w{2}-\w{4}', text)

    if len(frontal)>0: 
        try: 
            output={
                'Fecha de nacimiento': frontal[0],
                'Fecha expedicion': frontal[1]}
        except:  #case both date were not identified 
            output={
                'Fecha de nacimiento': 'DD-MMM-YYYY',
                'Fecha expedicion': 'DD-MMM-YYYY'         
            }
    else: 
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4)) 
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel,iterations=1) 
        invert = 255 - opening
        text=ocr(invert)
        number=re.findall('([0-9])',text)
        number_out=''.join(number)
        number_lines=text.splitlines()
        nombres=number_lines[8]
        apellidos=number_lines[6]
        output={
        'CC': number_out,
        'Nombres': nombres,
        'Apellidos': apellidos 
        }

    return output
