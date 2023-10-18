import cv2 as cv2
import pytesseract

def obtenerTexto(imagenes):
  # Usa Tesseract para extraer el texto
  texto = pytesseract.image_to_string(imagenes, lang="spa")  # `lang="spa"` si es en español

  return texto
