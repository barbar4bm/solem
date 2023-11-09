from flask import Flask
from routes import pruebas
from services import Sift as sift
from services import tools

app = Flask(__name__)

app.register_blueprint(pruebas.pruebas)

if __name__ == "__main__":
    sift.almacenar_descriptores()
    tools.cargarPaises()
    app.run(debug=True)
