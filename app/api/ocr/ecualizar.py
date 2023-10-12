import numpy as np
import cv2
import matplotlib.pyplot as plt

# Cargar la imagen
def cargar_imagen(ruta):
    try:
        img = cv2.imread(ruta)
        return img
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

# Cambio de espacio de color de BGR a RGB
def convertir_a_rgb(imagen):
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Ecualización
def ecualizar_imagen(imagen_gris):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    return clahe.apply(imagen_gris)

# Binarización
def binarizar_imagen(imagen_gris, umbral=127):
    ret, imagen_bin = cv2.threshold(imagen_gris, umbral, 255, cv2.THRESH_BINARY)
    return imagen_bin

# Binarización con Otsu
def binarizar_con_otsu(imagen_gris):
    ret, imagen_otsu = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return imagen_otsu

# Mostrar una imagen
def mostrar_imagen(imagen, cmap=None):
    plt.imshow(imagen, cmap=cmap, vmin=0, vmax=255)
    plt.axis('off')
    plt.show()

def procesar_imagen(ruta_imagen):
    try:
        # Cargar la imagen
        imagen = cv2.imread(ruta_imagen)

        # Verificar si la imagen se cargó correctamente
        if imagen is None:
            return 'No se pudo cargar la imagen', None

        # Convertir a RGB
        imagen_color = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # Convertir a escala de grises
        imagen_gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)

        # Procesar y mostrar la imagen
        imagen_ecualizada = ecualizar_imagen(imagen_gris)
        imagen_binarizada = binarizar_imagen(imagen_ecualizada)
        imagen_binarizada_otsu = binarizar_con_otsu(imagen_ecualizada)

        mostrar_imagen(imagen_color)
        mostrar_imagen(imagen_ecualizada, cmap='gray')
        mostrar_imagen(imagen_binarizada, cmap='gray')
        mostrar_imagen(imagen_binarizada_otsu, cmap='gray')

        return 'Procesamiento completado', imagen_color

    except Exception as e:
        return f'Error al procesar la imagen: {str(e)}', None

if __name__ == '__main__':
    resultado, imagen_procesada = procesar_imagen('Images/El_ejemplo_de_Cedula_identidad_Chile_2013.jpg')
    print(resultado)

