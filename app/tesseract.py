from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2

pytesseract.pytesseract.tesseract_cmd =r'c:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
image= pytesseract.image_to_string(Image.open('app/cedula.jpg'))
print(image)

