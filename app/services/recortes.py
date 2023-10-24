import tools as tool
import cv2 as cv2
import os

# Ruta del directorio que quieres listar
directorio = '.'

# Lista todos los archivos y directorios en el directorio especificado
archivos_y_directorios = os.listdir(directorio)

# Si solo quieres listar archivos y excluir directorios:
solo_archivos = [archivo for archivo in archivos_y_directorios if os.path.isfile(os.path.join(directorio, archivo))]

print("Todos los archivos y directorios:")
for item in archivos_y_directorios:
    print(item)

print("\nSolo archivos:")
for archivo in solo_archivos:
    print(archivo)

ruta = "app/services/"
anverso=cv2.imread(ruta+'8.1.jpg')
reverso=cv2.imread(ruta+'8.2.jpg')



recorte_dic=tool.recorte(anverso,reverso)
tool.guardar_recortes(recorte_dic)
