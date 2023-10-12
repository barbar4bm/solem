from pytesseract import Output
import cv2
from matplotlib import pyplot as plt

#encuadrar carnet
path_Example = 'OCR/single/nombre.png'
img_color = cv2.imread(path_Example)

#cambio de espacio de color
img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
plt.imshow(img_color)
plt.show()
data_image= pytesseract.image_to_data(invert, output_type=Output.DICT)

#cambiar colores a escala de grises
img_gris = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
plt.imshow(img_gris,'gray')
plt.show()

#binarizacion otsu
retval, thresh_img = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
plt.imshow(thresh_img,'gray')
plt.show()