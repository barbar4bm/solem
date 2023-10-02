from flask import Flask, jsonify, send_from_directory
import carnet
from api import ocr

app = Flask(__name__)

@app.route('/ocr')
def getOcr():
    return send_from_directory('app/api', ocr.py)

@app.route('/carnet')
def getCarnetCheck():
    return jsonify(carnet)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"

if __name__ == '__main__': 
    app.run(debug=True,port=5000)
