from flask import jsonify

import numpy as np
import cv2
import base64

from .Ocr import Ocr

IMAGE_PATH = 'app/images'

class ValidateCard():

    def base64_to_jpg(self, base64_string, output_path):
        # Eliminar el encabezado de la cadena base64 si está presente
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split('base64,')[1]

        # Decodificar la cadena base64 en una matriz numpy
        decoded_data = base64.b64decode(base64_string)
        np_data = np.frombuffer(decoded_data, np.uint8)

        # Decodificar la matriz numpy en una imagen OpenCV
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        # Guardar la imagen como JPG
        cv2.imwrite(f'{IMAGE_PATH}/{output_path}.jpg', img)

    def apply_validation(self, image_front: str, image_reverse: str):
        # transformar images

        self.base64_to_jpg(image_front, 'front')
        self.base64_to_jpg(image_reverse, 'reverse')

        ocr = Ocr()

        return ocr.applyOcr()
