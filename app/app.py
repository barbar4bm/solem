from flask import Flask, jsonify
from carnet import carnet 
import cv2
import sys
from PIL import Image
from pylab import * 






image = array(Image.open('app/asistencia.PNG'))
imshow(image)
# some points
x = [100,100,400,400]
y = [200,500,200,500]
plot(x,y,'r*')
plot(x[:2],y[:2])
title('Plotting: "asistencia"')
show()

