from flask import Flask, request,Response, jsonify,render_template
from routes import identity_card
from services import tools as tool

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('subir.html')

@app.route('/subirImagen', methods=['POST'])
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
    image_np = tool.b64_openCV(image_base64)
    
    # Convertir matriz numpy a imagen PNG
    png_bytes = tool.numpy_to_png(image_np)

    # Enviar imagen PNG al cliente
    return Response(png_bytes, content_type='image/png')


@app.route('/leerqr', methods=['POST'])
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

    # Convertir la imagen en una matriz
    imagenp = tool.imagen_a_matriz(file)  # Asumiendo que esta función acepta un objeto de archivo

    # Leer QR desde la matriz
    textoleido = tool.leerQR(imagenp)

    # Retornar el contenido leído
    return jsonify({'contenido_qr': textoleido})
    

if __name__ == "__main__":
    app.run(debug=True)
