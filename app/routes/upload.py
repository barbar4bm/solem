from flask import Blueprint, Response, render_template, request, jsonify,json
from services import cedula_chile

upload=Blueprint('obtener_json',__name__)

@upload.route('/upload_json', methods=['POST'])
def upload_json():
    # Verificar si se envió un archivo
    if 'anverso_reverso_b64' in request.files:
        file = request.files['anverso_reverso_b64']

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
    
    datos_respuesta=cedula_chile.procesar_imgenes_cedula(data)

    return jsonify(datos_respuesta)