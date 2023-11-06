from flask import jsonify
import pytesseract

import cv2

IMAGE_PATH = 'app/images'

class Ocr():
    def __init__(self) -> None:
        self.image_front = cv2.imread(f'{IMAGE_PATH}/front.jpg')
        self.image_reverse = cv2.imread(f'{IMAGE_PATH}/reverse.jpg')

    def get_text_by_image(self, imagen):
        texto = pytesseract.image_to_string(imagen)
        return str(texto)
    
    def limpiar_datos(self, ocr_result):
        cleaned_data = str(ocr_result).replace('\n', '').replace(' ', '').replace('<', '').replace('>', '').replace('.', '').replace('-', '').replace(',', '').replace(')', '').replace('(', '').split()
        return cleaned_data

    def apply_filters(self, image):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Cambio de espacio de color BGR a GRAY
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # Ecualización
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        
        rut_eq = clahe.apply(gray)

        cv2.equalizeHist(rut_eq)

        # Binarización
        ret, rut_bin = cv2.threshold(rut_eq,100,255,cv2.THRESH_BINARY)

        # Binarización otsu
        ret2, rut_otsu = cv2.threshold(rut_eq,127,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return (rut_bin, rut_otsu)

    def read_image_front(self, rut_bin_front):
        datos_front = {
            'nombre_texto': rut_bin_front[171:211 , 291:806], #nombre check
            'apellido_texto': rut_bin_front[88:152 , 292:520], #apellido check
            'rut_grande': rut_bin_front[460:496 , 98:273], #rut grande check
            'nacionalidad': rut_bin_front[220:265, 291:425], #nacionalidad check
            'sexo': rut_bin_front[229:257, 486:509], #no detecta solo un caracter
            'fecha_nacimiento': rut_bin_front[276:311 , 250:480], #fecha nacimiento check
            'doc_texto': rut_bin_front[275:310, 487:663], #numero documento check
            'fecha_emision': rut_bin_front[330:369 , 292:463], #fecha emision check
            'fechaV_texto': rut_bin_front[328:370 , 473:670] #fecha vencimiento check
        }

        return datos_front

    def read_image_reverse(self, rut_bin_reverse, rut_otsu_reverse):
        datos_reverse = {
            'nacio_en': rut_bin_reverse[211:247 , 182:600] ,
            'profesion': rut_bin_reverse[242:274 , 182:403],
            'mrz': rut_otsu_reverse[354:492 , 42:800],
            'nacionalidad_doc_mrz': rut_otsu_reverse[343:398 , 37:800],
            'fechas_rut_mrz':rut_otsu_reverse[390:436 , 37:800],
            'nombre_full_mrz': rut_otsu_reverse[432:482 , 37:800]
        }

        return datos_reverse
    
    def get_text_by_ocr_front(self, datos_front):
        datos_front_text = {
            'data_nombre': self.limpiar_datos(self.get_text_by_image(datos_front['nombre_texto'])),
            'data_apellido': self.limpiar_datos(self.get_text_by_image(datos_front['apellido_texto'])),
            'data_fecha_nacimiento': self.limpiar_datos(self.get_text_by_image(datos_front['fecha_nacimiento'])),
            'data_rut_grande': self.limpiar_datos(self.get_text_by_image(datos_front['rut_grande'])),
            'data_nacionalidad': self.limpiar_datos(self.get_text_by_image(datos_front['nacionalidad'])),
            'data_fecha_emision': self.limpiar_datos(self.get_text_by_image(datos_front['fecha_emision'])),
            'data_fechaV_texto': self.limpiar_datos(self.get_text_by_image(datos_front['fechaV_texto'])),
            'data_numero_doc': self.limpiar_datos(self.get_text_by_image(datos_front['doc_texto'])),
        }

        datos_front_text['data_apellido_nombre'] = datos_front_text['data_apellido'][0] + datos_front_text['data_nombre'][0]

        return datos_front_text
    
    def get_text_by_ocr_reverse(self, datos_reverse):
        datos_reverse_text = {
            'data_nacionalidad_doc_mrz': self.limpiar_datos(self.get_text_by_image(datos_reverse['nacionalidad_doc_mrz'])),
            'data_fechas_rut_mrz': self.limpiar_datos(self.get_text_by_image(datos_reverse['fechas_rut_mrz'])),
            'data_nombre_full_mrz': self.limpiar_datos(self.get_text_by_image(datos_reverse['nombre_full_mrz']))
        }

        return datos_reverse_text

    def applyOcr(self):
        rut_bin_front, rut_otsu_front = self.apply_filters(self.image_front)
        rut_bin_reverse, rut_otsu_reverse = self.apply_filters(self.image_reverse)
        
        datos_front = self.read_image_front(rut_bin_front)
        datos_reverse = self.read_image_reverse(rut_bin_reverse, rut_otsu_reverse)
        
        datos_front_text = self.get_text_by_ocr_front(datos_front)
        print(datos_front_text)
    
        datos_reverse_text = self.get_text_by_ocr_reverse(datos_reverse)
        print(datos_reverse_text)

        return jsonify({'success': True })