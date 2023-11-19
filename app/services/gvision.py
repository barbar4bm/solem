import json
import requests
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from services import tools

def guardar_json(diccionario, nombre_archivo):
    with open(f'{nombre_archivo}.json', 'w') as file:
        file.write(json.dumps(diccionario,indent=4))
    return

def procesamiento_gvision(diccionario_img,nombre_persona):
    print('gvision')

    #convertir a b64 cada imagen

    dic_b64=tools.convertir_diccionario_a_base64(diccionario_img)
    

    """with open('diccionario_base64.txt', 'w') as file:
        file.write(diccionario)
    """


    # Obtener el directorio base (donde se encuentra el archivo Python actual)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta hacia ocr-gv.json
    archivo_credenciales = os.path.join(BASE_DIR, 'data', 'ocr-gv.json')
    # Verificar si el archivo existe
    existe_archivo = os.path.exists(archivo_credenciales)
    print(f"La ruta del archivo de credenciales es: {archivo_credenciales}")
    print(f"¿Existe el archivo de credenciales? {existe_archivo}")


    dic_respuesta=enviar_a_google_vision(dic_b64,archivo_credenciales)
    lista_text=extraer_texto_reconocido(dic_respuesta)
    
    with open(f'{nombre_persona}.txt', 'w', encoding='utf-8') as f:
        for item in lista_text:
            f.write("%s\n" % item)

    return lista_text


def cargar_credenciales(archivo_json):
    
    # Cargar las credenciales desde el archivo JSON
    credenciales = service_account.Credentials.from_service_account_file(
        archivo_json,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Obtener un token de acceso
    credenciales.refresh(Request())
    return credenciales.token

def enviar_solicitud(url, headers, body):
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        print('200')
        return response.json()
    else:
        return {"Error": response.status_code, "Message": response.text}
    

def extraer_texto_reconocido(respuesta_json):
    """
    Extrae todos los textos reconocidos de la respuesta de la API de Google Vision.

    :param respuesta_json: Respuesta JSON de la API de Google Vision.
    :return: Lista de textos reconocidos.
    """
    # Cargar el JSON
    datos = json.loads(respuesta_json)

    # Lista para almacenar todos los textos reconocidos
    textos_reconocidos = []

    # Recorrer cada respuesta y extraer el texto reconocido
    for respuesta in datos['responses']:
        if 'fullTextAnnotation' in respuesta:
            textos_reconocidos.append(respuesta['fullTextAnnotation']['text'])

    return textos_reconocidos

def enviar_a_google_vision(diccionario_img, archivo_credenciales):
    # Valor predeterminado para el máximo de imágenes por solicitud
    max_images_per_request = 16

    # Cargar credenciales
    token_acceso = cargar_credenciales(archivo_credenciales)

    url = "https://vision.googleapis.com/v1/images:annotate"
    headers = {"Authorization": f"Bearer {token_acceso}"}

    # Dividir las solicitudes
    all_responses = []  # Lista para almacenar las respuestas de todas las solicitudes
    partial_request = {"requests": []}
    count = 0
    for clave, imagen_base64 in diccionario_img.items():
        partial_request["requests"].append({
            "image": {"content": imagen_base64},
            "features": [{"type": "TEXT_DETECTION"}]
        })
        count += 1

        # Enviar solicitud si se alcanza el límite máximo por solicitud
        if count >= max_images_per_request:
            response = enviar_solicitud(url, headers, partial_request)
            all_responses.extend(response.get('responses', []))
            partial_request = {"requests": []}
            count = 0

    # Enviar cualquier solicitud restante
    if count > 0:
        response = enviar_solicitud(url, headers, partial_request)
        all_responses.extend(response.get('responses', []))

    # Devolver las respuestas en formato JSON
    return json.dumps({"responses": all_responses})

def extraer_texto_reconocido(respuesta_json):
    """
    Extrae todos los textos reconocidos de la respuesta de la API de Google Vision.

    :param respuesta_json: Respuesta JSON de la API de Google Vision.
    :return: Lista de textos reconocidos.
    """
    # Cargar el JSON
    datos = json.loads(respuesta_json)

    # Lista para almacenar todos los textos reconocidos
    textos_reconocidos = []

    # Recorrer cada respuesta y extraer el texto reconocido
    for respuesta in datos['responses']:
        if 'fullTextAnnotation' in respuesta:
            textos_reconocidos.append(respuesta['fullTextAnnotation']['text'])

    return textos_reconocidos

# Uso de la función
# respuesta_json = 'Aqui va tu JSON de respuesta de la API'
# textos = extraer_texto_reconocido(respuesta_json)
# for texto in textos:
#     print(texto)