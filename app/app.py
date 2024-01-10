from flask import Flask
from routes import pruebas
from routes import upload
from services import Sift as sift

app = Flask(__name__)

app.register_blueprint(pruebas.pruebas)
app.register_blueprint(pruebas.subir)
app.register_blueprint(upload.upload)


if __name__ == "__main__":
    sift.almacenar_descriptores()
    app.run(port=5000, debug=False)
