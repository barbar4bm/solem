from flask import Blueprint, Response, render_template, request, jsonify,json
from services import Ocr,tools
from services import Sift as sift
from services import cropper
from services.carnet import Cedula
from services import validacion as validar
from services import cedula_chile

pruebas = Blueprint('pruebas', __name__)
subir=Blueprint('subir',__name__)

@pruebas.route('/subir', methods=['GET'])
def show_subir():
    # Solo mostrar la página
    return render_template('subir.html')

@pruebas.route('/pruebas', methods=['GET'])
def show_pruebas():
    # Solo mostrar la página
    return render_template('pruebas.html')

@pruebas.route('/upload', methods=['POST'])
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

@pruebas.route('/leerqr', methods=['POST'])
def enviarContenidoQr():
    # Comprobar que la solicitud contiene un archivo
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    # Comprobar que el archivo no está vacío y que es una imagen
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file or not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Invalid image format'}), 400

    # Leer el archivo en bytes
    image_data = file.read()

    # Convertir la imagen en una matriz
    imagenp = tools.imagen_a_matriz(image_data)

    # Leer QR desde la matriz
    textoleido = tools.leerQR(imagenp)

    # Retornar el contenido leído
    return jsonify({'contenido_qr': textoleido})

@pruebas.route('/subirImagen', methods=['POST'])
def recibirImagenes():
    
    # Si el request contiene un archivo
    if 'file' in request.files:
        file = request.files['file']
        
        # Asegurarse de que el archivo no está vacío
        if file.filename == '':
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400
        
        # Leer el contenido del archivo
        content = file.read().decode('utf-8')  # Asumimos que el contenido del archivo txt es una cadena base64

        # Aquí puedes añadir cualquier validación adicional que necesites, por ejemplo, verificar que el contenido es una cadena base64 válida.
        
        image_base64 = content
        
    # Si el request es un JSON
    elif request.is_json:
        data = request.get_json()
        image_base64 = data.get('imagen')  # Suponemos que la clave en el JSON es 'imagen'
        if not image_base64:
            return jsonify({"error": "El JSON no contiene la clave 'imagen'"}), 400

    else:
        return jsonify({"error": "El request debe ser un archivo o un JSON"}), 400

    # Convertir de base64 a matriz numpy
    image_np = tools.b64_openCV(image_base64)
    
    # Convertir matriz numpy a imagen PNG
    png_bytes = tools.numpy_to_png(image_np)

    # Enviar imagen PNG al cliente
    return Response(png_bytes, content_type='image/png')



