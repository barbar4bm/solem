import cv2
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt



#reading image
img1 = cv2.imread('El_ejemplo_de_Cedula_identidad_Chile_2013.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

#keypoints
sift = cv2.xfeatures2d.SIFT_create()
sift = cv2.xfeatures2d.SIFT_create(0, 3, 0.09, 0, 2)
keypoints_1, descriptors_1 = sift.detectAndCompute(rut_eq,None)


img_sift = cv2.drawKeypoints(rut_eq,keypoints_1,img_rgb)

img_sift=cv2.drawKeypoints(rut_eq, keypoints_1, rut_eq,
                      flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.figure(figsize=(16, 12), dpi=200)
plt.imshow(img_sift)

#Cálculo de la homografía (relacionar descriptores)

def equalize(image):
  # Cambio de espacio de color de BGR a RGB
  img_rgb = cv2.cvtColor(image, cv.COLOR_BGR2RGB)
  # Cambio de espacio de color BGR a GRAY
  gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
  # Ecualización
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
  rut_eq = clahe.apply(gray)

  return rut_eq


MIN_MATCH_COUNT = 10
#img1 = cv.imread('20221214_153703.jpg',0)          # queryImage
img1 = equalize(cv.imread('Images/20221214_153726.jpg'))          # queryImage
img2 = equalize(cv.imread('Images/El_ejemplo_de_Cedula_identidad_Chile_2013.jpg')) # trainImage

# Initiate SIFT detector
#sift = cv.SIFT_create()
sift = cv2.xfeatures2d.SIFT_create(0, 3, 0.04, 10, 1.6)
# find the keypoints and descriptors with SIFT
kp_obj, des_obj = sift.detectAndCompute(img1,None) # query
kp_scene, des_scene = sift.detectAndCompute(img2,None) # train
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des_obj,des_scene,k=2)
# store all the good matches as per Lowe's ratio test.
good = []
dst = None
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)