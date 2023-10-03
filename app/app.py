from flask import Flask, jsonify
from carnet import carnet 
import cv2
import sys 

app = Flask(__name__)


@app.route('/carnet')
def getCarnetCheck():
    return jsonify(carnet)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"


def main():
    if len(sys.argv) < 2:
        print("Por favor, proporciona la ruta de la imagen como argumento.")
        return
    
    img = cv2.imread(sys.argv[1])
    
    if img is None:
        print("No se pudo cargar la imagen.")
        return
    
    cv2.namedWindow("Example1", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Example1", img)
    cv2.waitKey(0)
    cv2.destroyWindow("Example1")


if __name__ == '__main__': 
    app.run(debug=True,port=5000)