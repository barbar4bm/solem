from flask import Flask, jsonify
import carnet
from routes.auth import routes_auth

app = Flask(__name__)

@app.route('/ocr')
def getOcr():
   print('hola')
   return None

@app.route('/carnet')
def getCarnetCheck():
    return jsonify(carnet)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"

if __name__ == '__main__': 
    #load_dotenv()
    app.register_blueprint(routes_auth, url_prefix='/auth')
    app.run(debug=True,port=5000)
