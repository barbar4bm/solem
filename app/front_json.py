from flask import Flask, jsonify
import cv2
from PIL import Image
from pylab import *
import pytesseract

app = Flask(__name__)

def OCR(imagen):
    texto = pytesseract.image_to_string(imagen)
    return texto

@app.route('/procesar_imagen', methods=['POST'])
def procesar_imagen():
    image = cv2.imread('app/image/a7.jpg')

    # Conversión a escala de grises
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Ecualización
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized = clahe.apply(gray)

    # Binarización
    _, binarized = cv2.threshold(equalized, 100, 255, cv2.THRESH_BINARY)

    # Binarización con Otsu
    _, binarized_otsu = cv2.threshold(equalized, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Definición de regiones de interés
    nombre = binarized[171:211, 291:810]  # nombre check
    apellido = binarized[85:152, 292:520]  # apellido check
    rut_grande = binarized[460:496, 98:273]  # rut grande check
    nacionalidad = binarized[220:265, 291:425]  # nacionalidad check
    sexo = binarized_otsu[222:263, 450:600]  # no detecta género
    fecha_nacimiento = binarized[276:311, 250:480]  # fecha de nacimiento check
    numero_docu = binarized[275:310, 487:663]  # número de documento check
    fecha_emision = binarized[330:369, 292:463]  # fecha de emisión check
    fecha_vencimiento = binarized[335:367, 477:667]  # fecha de vencimiento check
    rut_chico = binarized_otsu[282:308, 686:808]  # rut en foto pequeña falta mejorar su visibilidad

    # Mostrar imágenes
    plt.imshow(nombre, cmap='gray')
    show()
    # Mostrar el resto de las imágenes

    # Realizar la extracción de texto de las regiones de interés
    nombres = OCR(nombre)
    apellidos = OCR(apellido)
    rut_grande_texto = OCR(rut_grande)
    nacionalidad_texto = OCR(nacionalidad)
    sexo_texto = OCR(sexo)
    fecha_nacimiento_texto = OCR(fecha_nacimiento)
    numero_docu_texto = OCR(numero_docu)
    fecha_emision_texto = OCR(fecha_emision)
    fecha_vencimiento_texto = OCR(fecha_vencimiento)
    rut_chico_texto = OCR(rut_chico)

    # Crear el diccionario de respuesta
    response = {
        "Nombres": nombres,
        "Apellidos": apellidos,
        "Rut grande": rut_grande_texto,
        "Nacionalidad": nacionalidad_texto,
        "Sexo": sexo_texto,
        "Fecha de nacimiento": fecha_nacimiento_texto,
        "Numero de documento": numero_docu_texto,
        "Fecha de emisión": fecha_emision_texto,
        "Fecha de vencimiento": fecha_vencimiento_texto,
        "Rut pequeño": rut_chico_texto
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
