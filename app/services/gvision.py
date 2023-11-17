import base64
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

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
        return response.json()
    else:
        return {"Error": response.status_code, "Message": response.text}
    

def procesar_respuestas_vision(respuestas, claves_imagenes):
    """
    Procesa las respuestas de la API de Google Vision y extrae el texto reconocido.
    
    :param respuestas: Lista de respuestas de la API de Google Vision.
    :param claves_imagenes: Lista de claves de las imágenes enviadas.
    :return: Diccionario con las claves de las imágenes y el texto reconocido.
    """
    texto_reconocido = {}

    for clave, respuesta in zip(claves_imagenes, respuestas):
        # Asumimos que cada respuesta corresponde a una imagen en claves_imagenes
        if respuesta['responses']:
            # Extraemos el texto completo (el primer elemento de textAnnotations contiene el texto completo)
            texto = respuesta['responses'][0].get('fullTextAnnotation', {}).get('text', '')
            texto_reconocido[clave] = texto
            print(clave, ' ',texto)

    return texto_reconocido

def enviar_a_google_vision(diccionario_img, archivo_credenciales, max_images_per_request=10):
    # ... (código de carga de credenciales)

    url = "https://vision.googleapis.com/v1/images:annotate"
    token_acceso = cargar_credenciales(archivo_credenciales)
    headers = {"Authorization": f"Bearer {token_acceso}"}

    # Dividir las solicitudes
    responses = []
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
            responses.append(response)
            partial_request = {"requests": []}
            count = 0

    # Enviar cualquier solicitud restante
    if count > 0:
        response = enviar_solicitud(url, headers, partial_request)
        responses.append(response)

    return responses
# Ejemplo de uso
# archivo_credenciales = "path_to_your_credentials.json"
# diccionario_img = {"clave1": imagen1_base64, "clave2": imagen2_base64, ...}
# resultado = enviar_a_google_vision(diccionario_img, archivo_credenciales)
