from flask import Flask, jsonify
from carnet import carnet 
import cv2 
from PIL import Image
import pytesseract

app = Flask(__name__)



@app.route('/carnet')
def getCarnetCheck():
    return jsonify(carnet)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"

if __name__ == '__main__': 
    app.run(debug=True,port=5000)

im_file = "imagen" #nombre de la imagen, debe de ser una cedula
im = Image.open(im_file)
