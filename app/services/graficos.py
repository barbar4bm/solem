from matplotlib import pyplot as plt
import cv2 as cv2
import numpy as np
    
def mostrarImagen(img, titulo='',cmap='gray'):
  plt.title(titulo)
  plt.imshow(img,cmap)
  plt.show()  
  
def imprimirHistograma(imagenGray,titulo,ejex,ejey):
   # Calcular el histograma de la imagen en escala de grises
  hist = cv2.calcHist([imagenGray], [0], None, [256], [0, 256])
  # Mostrar el histograma
  plt.figure()
  plt.title(titulo)
  plt.xlabel(ejex)
  plt.ylabel(ejey)
  plt.bar(range(256), hist[:,0], width=1.0, color='b')
  plt.xlim([0, 256])
  plt.show()
  plt.imshow(imagenGray, cmap='gray', vmin=0, vmax=255)

def mostrarPuntos(imagen,puntos):
  img_sift=cv2.drawKeypoints(imagen, puntos, imagen,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  plt.figure(figsize=(6, 4), dpi=200)
  plt.imshow(img_sift)


def mostrarEncuadre(img,dst):
    #mostrar los poligonos como lineas de color negro para indicar en img1 las uniones de los puntos contenidos en dst
    imgpolig = cv2.polylines(img,[np.int32(dst)],True,0,20, cv2.LINE_AA)

    plt.imshow(imgpolig, cmap='gray')  # usa cmap='gray' solo si es una imagen en escala de grises
    plt.axis('off')  # para ocultar los ejes
    plt.show()  

def mostrarCorrespondencias(matchesMask,imgEq,kp_obj,img_ref,kp_ref,good):
  draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)
  img3 = cv2.drawMatches(imgEq,kp_obj,img_ref,kp_ref,good,None,**draw_params)

  plt.figure(figsize=(6, 4), dpi=300)
  plt.imshow(img3, 'gray'),plt.show()   

