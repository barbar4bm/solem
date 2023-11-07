from flask import Blueprint, render_template, request, jsonify,json
from services import Ocr,tools
from services import Sift as sift
from services import cropper
from services.carnet import Cedula

pruebas = Blueprint('pruebas', __name__)

@pruebas.route('/pruebas', methods=['GET'])
def show_pruebas():
    # Solo mostrar la página
    return render_template('pruebas.html')

@pruebas.route('/upload', methods=['POST'])
def upload_json():
    # Verificar si se envió un archivo
    if 'archivo_json' in request.files:
        file = request.files['archivo_json']

        # Asegurarse de que el archivo tenga un nombre (es decir, que no esté vacío)
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

        # Leer el archivo JSON
        json_content = file.read()

        try:
            data = json.loads(json_content)
        except Exception as e:
            return jsonify({'error': 'Error al analizar el archivo JSON'}), 400
    else:
        # Si no se envió un archivo, intentar obtener el objeto JSON del cuerpo de la solicitud
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No se envió ningún archivo ni objeto JSON'}), 400

    # Verificar que las claves 'anverso' y 'reverso' estén presentes
    if 'anverso' not in data or 'reverso' not in data:
        return jsonify({'error': 'El archivo JSON no contiene clave anverso o reverso'}), 400

    # Convertir las imágenes de base64 a objetos de imagen
    anverso=tools.b64_openCV(data['anverso'])
    reverso=tools.b64_openCV(data['reverso'])

    anverso=sift.preparacionInicial(anverso)
    reverso=sift.preparacionInicial(reverso)

    #aqui se usa SIFT para ver si coinciden los descriptores
    #retorna booleano
    resp_Anverso,resp_reverso=sift.identificador_lados(anverso,reverso)

    #atratapar cuando alguno es falso y generar jSON respuesta
    #aqui se llama a alguna funcion de codeJSON


    if resp_Anverso and not resp_reverso:
        return jsonify({'ocr_data': 'Solo se reconoce Anverso'})
    elif not resp_Anverso and resp_reverso:
        return jsonify({'ocr_data': 'Solo se reconoce Reverso'})
    elif not resp_Anverso and not resp_reverso:
        return jsonify({'ocr_data': 'No se reconoce como Cedula'})


    resp_Anverso=str(resp_Anverso)
    resp_reverso=str(resp_reverso)

    diccionario_img=cropper.recorte(anverso,reverso)
    
    clave_omitida=('qr','textoGeneral_MRZ','mrz_raw','linea1','linea2','linea3')

    diccionario_ocr = Ocr.obtenerTexto(diccionario_img,*clave_omitida)

    carnet=Cedula(diccionario_ocr)
    

    datos_respuesta={
        'ocr_data': vars(carnet),
        'resp_Anverso': resp_Anverso,
        'resp_reverso': resp_reverso
    }
    
    return  jsonify(datos_respuesta)

@pruebas.route('/ocr', methods=['POST'])
def procesar_ocr():
    # Verificar que la imagen esté presente en la solicitud
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400

    image_file = request.files['image']

    # Asegurarse de que la imagen tenga un nombre (es decir, que no esté vacía)
    if image_file.filename == '':
        return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400

    # Convertir la imagen recibida a un formato utilizable para el OCR
    image_data = image_file.read()
    image_data=tools.imagen_a_matriz(image_data)
    textoCap=Ocr.aplicarOCR(image_data)
    # Procesar la imagen con la función OCR
    # Asumo que la función Ocr.process() es la que se encarga de esto, si no, reemplázalo por la función adecuada.
  

    # Devolver el texto obtenido
    return textoCap


@pruebas.route('/subir', methods=['POST'])
def subir():
    # Verificar si se envió un archivo
    if 'archivo_json' in request.files:
        file = request.files['archivo_json']

        # Asegurarse de que el archivo tenga un nombre (es decir, que no esté vacío)
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

        # Leer el archivo JSON
        json_content = file.read()

        try:
            data = json.loads(json_content)
        except Exception as e:
            return jsonify({'error': 'Error al analizar el archivo JSON'}), 400
    else:
        # Si no se envió un archivo, intentar obtener el objeto JSON del cuerpo de la solicitud
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No se envió ningún archivo ni objeto JSON'}), 400

    # Verificar que las claves 'anverso' y 'reverso' estén presentes
    if 'anverso' not in data or 'reverso' not in data:
        return jsonify({'error': 'El archivo JSON no tiene la estructura esperada'}), 400

    # Convertir las imágenes de base64 a objetos de imagen
    anverso=tools.b64_openCV(data['anverso'])
    reverso=tools.b64_openCV(data['reverso'])

    anverso=sift.preparacionInicial(anverso)
    reverso=sift.preparacionInicial(reverso)

    #aqui se usa SIFT para ver si coinciden los descriptores
    #retorna booleano
    resp_Anverso,resp_reverso=sift.identificador_lados(anverso,reverso)

    #atratapar cuando alguno es falso y generar jSON respuesta
    #aqui se llama a alguna funcion de codeJSON

    resp_Anverso=str(resp_Anverso)
    resp_reverso=str(resp_reverso)

    diccionario_img=cropper.recorte(anverso,reverso)
    clave_omitida=('qr','textoGeneral_MRZ','mrz_raw','linea1','linea2','linea3')

    diccionario_ocr = Ocr.obtenerTexto(diccionario_img,*clave_omitida)
    

    carnet=Cedula(diccionario_ocr)
    

    datos_respuesta={
        'ocr_data': vars(carnet),
        'resp_Anverso': resp_Anverso,
        'resp_reverso': resp_reverso
    }
    
    return  jsonify(datos_respuesta)