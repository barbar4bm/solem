from PIL import Image
import pytesseract


# Abrimos la imagen
im = Image.open("example_01.png")


# Le pasamos como argumento la imagen abierta con Pillow
texto = pytesseract.image_to_string(im)

print(texto)