from flask import Flask
from routes import pruebas
from services import Sift as sift
from services import cedula_chile

app = Flask(__name__)

app.register_blueprint(pruebas.pruebas)


if __name__ == "__main__":
    sift.almacenar_descriptores()
    cedula_chile.esWin()
    app.run(port=5002, debug=True)
