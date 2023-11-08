from flask import Flask
from routes import pruebas
from services import Sift as sift

app = Flask(__name__)

app.register_blueprint(pruebas.pruebas)

if __name__ == "__main__":
    sift.guardarDescriptores()
    app.run(debug=True)
