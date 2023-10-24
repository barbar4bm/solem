from flask import Blueprint, render_template, request, jsonify
from services import Ocr,tools

pruebas = Blueprint('pruebas', __name__)

@pruebas.route('/pruebas', methods=['GET'])
def show_pruebas():
    # Solo mostrar la página
    return render_template('pruebas.html')

@pruebas.route('/upload', methods=['POST'])
def upload_json():
    # Verificar que el archivo esté presente en la solicitud
    if 'archivo_json' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400

    file = request.files['archivo_json']

    # Asegurarse de que el archivo tenga un nombre (es decir, que no esté vacío)
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
    # Aquí puedes agregar cualquier validación adicional si es necesario.

    # Leer el archivo JSON
    json_content = file.read()

    # Aquí puedes procesar el contenido del JSON como lo necesites.
    return jsonify({'message': 'Archivo JSON recibido con éxito!'})

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
    imgnp=tools.imagen_a_matriz(image_data)
    textoCap=Ocr.obtenerTexto(imgnp)
    # Procesar la imagen con la función OCR
    # Asumo que la función Ocr.process() es la que se encarga de esto, si no, reemplázalo por la función adecuada.
  

    # Devolver el texto obtenido
    return textoCap