from flask import Flask, jsonify
from carnet import carnet 


app = Flask(__name__)


@app.route('/carnet')
def getCarnetCheck():
    return jsonify(carnet)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"

if __name__ == '__main__': 
    app.run(debug=True,port=5000)