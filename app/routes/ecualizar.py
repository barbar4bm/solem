from flask import Blueprint, request, jsonify
from ecualizar import procesar_imagen

routes_auth = Blueprint("test", __name__)

@routes_auth.route("/ecualizar", methods=["POST"])
def ecualizar():
    try:
        data = request.get_json()
        if "imagen" in data:
            resultado, imagen_procesada = procesar_imagen(data["imagen"])
            if resultado == 'Procesamiento completado':
                return jsonify({"message": "Procesamiento exitoso", "imagen_procesada": imagen_procesada.tolist()})
            else:
                response = jsonify({"message": resultado})
                response.status_code = 400
                return response
        else:
            response = jsonify({"message": "No se proporcionó la imagen en la solicitud"})
            response.status_code = 400
            return response
    except Exception as e:
        response = jsonify({"message": f"Ha ocurrido un error: {str(e)}"})
        response.status_code = 500
        return response
