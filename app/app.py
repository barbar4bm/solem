from flask import Flask, request,Response, jsonify
from routes import identity_card
from services import tools as tool
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"

@app.route('/post', methods=['POST'])
def recibirImagenes():
    if not request.is_json:
        return jsonify({"error": "El request debe ser un JSON"}), 400

    data = request.get_json()
    image_base64 = data.get("imagen1")  #"imagen1" es la clave en el JSON

    # Convertir de base64 a matriz numpy
    image_np = tool.b64_openCV(image_base64)

    # Convertir matriz numpy a imagen PNG
    png_bytes = tool.numpy_to_png(image_np)

    # Enviar imagen PNG al cliente
    return Response(png_bytes, content_type='image/png')