from flask import Flask
from routes import pruebas
from services import Sift as sift
from services import cedula_chile

app = Flask(__name__)

app.register_blueprint(pruebas.pruebas)
app.register_blueprint(pruebas.subir)


if __name__ == "__main__":
    sift.almacenar_descriptores()
    app.run(host='0.0.0.0',port=5000, debug=True)

