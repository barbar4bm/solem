from flask import Flask, jsonify
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

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

@app.route('/')
def procesar_imagen():
    image = cv2.imread('app/image/24.3.jpg')

    title('Cedula de Identidad')

    # Cambio de espacio de color de BGR a RGB
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Cambio de espacio de color BGR a GRAY
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Ecualización
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    rut_eq = clahe.apply(gray)

    # Binarización
    ret, rut_bin = cv2.threshold(rut_eq, 100, 255, cv2.THRESH_BINARY)

    # Binarización otsu
    ret2, rut_otsu = cv2.threshold(rut_eq, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Lectura trasera
    nacio_en = rut_bin[211:247, 182:600]  # check pero con detalles
    profesion = rut_bin[242:274, 182:403]
    mrz = rut_otsu[354:492, 42:800]

    gray2 = cv2.medianBlur(mrz, 5)
    dst2 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    result = {
        "Nacio en": OCR(nacio_en),
        "Profesion": OCR(profesion),
        "MRZ": OCR(mrz)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
