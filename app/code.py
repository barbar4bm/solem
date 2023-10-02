
import cv2 
from PIL import Image
import matplotlib.pyplot as plt
import pickle
import pywt
import pywt.data


im_file = "imagen" #nombre de la imagen, debe de ser una cedula
im = Image.open(im_file)

#BGR a RGB luego de RGB a GRAY
img_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# Ecualización
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
rut_eq = clahe.apply(gray)
# Binarización
ret,rut_bin = cv2.threshold(rut_eq,127,255,cv2.THRESH_BINARY)
# Binarización otsu
ret2,rut_otsu = cv2.threshold(rut_eq, 127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

plt.imshow(img_rgb)
plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
plt.imshow(rut_eq, cmap='gray', vmin=0, vmax=255)
plt.imshow(rut_bin, cmap='gray', vmin=0, vmax=255)
plt.imshow(rut_otsu, cmap='gray', vmin=0, vmax=255) 

#reading image
#img1 = cv2.imread('El_ejemplo_de_Cedula_identidad_Chile_2013.jpg')
#gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

#keypoints
#sift = cv2.xfeatures2d.SIFT_create()
sift = cv2.xfeatures2d.SIFT_create(0, 3, 0.01, 4, 1.6)
keypoints_1, descriptors_1 = sift.detectAndCompute(rut_eq,None)


#img_sift = cv2.drawKeypoints(rut_eq,keypoints_1,img_rgb)

img_sift=cv2.drawKeypoints(rut_eq, keypoints_1, rut_eq,
                      flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.figure(figsize=(16, 12), dpi=200)
plt.imshow(img_sift)

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

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


if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp_obj[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp_scene[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv.findHomography(dst_pts, src_pts, cv.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    h,w = img2.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv.perspectiveTransform(pts,M)
    img1 = cv.polylines(img1,[np.int32(dst)],True,255,20, cv.LINE_AA)
else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

print(np.int32(dst))

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)
img3 = cv.drawMatches(img1,kp_obj,img2,kp_scene,good,None,**draw_params)

img3 = cv.circle(img3, (2730, 436), 50, (255, 0, 0), 20)
img3 = cv.circle(img3, (674, 583), 50, (0, 255, 0), 20)
img3 = cv.circle(img3, (855, 3893), 50, (0, 0, 255), 20)
plt.figure(figsize=(10, 8), dpi=200)
plt.imshow(img3, 'gray'),plt.show()

# Uso los puntos calculados en dst

srcTri = np.array( [[2730, 436], [674, 583], [855, 3893]] ).astype(np.float32)
dstTri = np.array( [[0, 0], [0, 300], [500, 300]] ).astype(np.float32)
warp_mat = cv.getAffineTransform(srcTri, dstTri)
warp_dst = cv.warpAffine(img1, warp_mat, (500, 300))

plt.figure(figsize=(5, 4), dpi=200)
cv.rectangle(warp_dst, (20, 55), (150, 220), (255, 0,0), 4) #foto grande
cv.rectangle(warp_dst, (120, 10), (160, 40), (255, 0,0), 4) #bandera chile
cv.rectangle(warp_dst, (395, 110), (480, 170), (255, 0,0), 4) #foto pequeña
plt.imshow(warp_dst, 'gray'),plt.show()

img1 = cv.imread('Image/El_ejemplo_de_Cedula_identidad_Chile_2013.jpg',cv.IMREAD_GRAYSCALE)   # Train image

# Crear el detecto SIFT
sift = cv.SIFT_create()

# Guardo en un diccionario descriptores de mario
kp1, des1 = sift.detectAndCompute(img1,None)

dic = {"frente": des1}

# Guardo en disco los descriptores
with open('mi-base-de-datos.pkl', 'wb') as f:
  pickle.dump(dic, f)

  # Leo la matriz en el disco duro
with open('mi-base-de-datos.pkl', 'rb') as f:
  b = pickle.load(f)

desc_frente = b['frente']

# Calculo los descriptores de la imagen nueva
# Inicializo el detector SIFT

# Query Image
img_frente = cv.imread('Images/20221214_153726.jpg',cv.IMREAD_GRAYSCALE)
img_no_frente = cv.imread('Images/20221214_153707.jpg',cv.IMREAD_GRAYSCALE)

sift = cv.SIFT_create()

# Encuentro los descriptores de la imagen a revisar
kp1, des1 = sift.detectAndCompute(img_frente,None)

# Busco los descriptores que están más cerca
bf = cv.BFMatcher()
matches = bf.knnMatch(desc_frente, des1, k=2)

# Aplico test de cercanía
good = []
for m,n in matches:
    if m.distance < 0.5*n.distance:
        good.append([m])

coincidencias = len(good)
print(f'Número de coincidencia de descriptores: {coincidencias}')

if (coincidencias > 20):
  print('Carnet: Posición de frente')
else:
  print('No se reconoce carnet')

img_pantalla = cv.imread('Images/foto-pantalla.jpg', cv2.IMREAD_GRAYSCALE)
img_normal = cv.imread('Images/20221214_153703.jpg', cv2.IMREAD_GRAYSCALE)

plt.figure(figsize=(5, 4), dpi=200)
plt.imshow(img_pantalla, 'gray')
plt.show()

# Wavelet transform of image, and plot approximation and details
titles = ['Aprox', ' H',
          'V', 'D']
coeffs2 = pywt.dwt2(img_normal, 'bior1.3')
LL, (LH, HL, HH) = coeffs2
fig = plt.figure(figsize=(5, 4), dpi=200)

for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(2, 2, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])

fig.suptitle("Foto tomada desde un celular", fontsize=14)

# Now reconstruct and plot the original image
#reconstructed = pywt.idwt2(coeffs2, 'bior1.3')
#fig = plt.figure()
#plt.imshow(reconstructed, interpolation="nearest", cmap=plt.cm.gray)

# Wavelet transform of image, and plot approximation and details
titles = ['Aprox', ' H',
          'V', 'D']
coeffs2 = pywt.dwt2(img_pantalla, 'bior1.3')
LL, (LH, HL, HH) = coeffs2
fig = plt.figure(figsize=(5, 4), dpi=200)

for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(2, 2, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])

fig.suptitle("Imagen desde pantalla", fontsize=14)