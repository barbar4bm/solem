from flask import Blueprint, render_template, request, jsonify,json
from services import Ocr,tools
from services import Sift as sift
from services import cropper
from services.carnet import Cedula

pruebas = Blueprint('pruebas', __name__)

@pruebas.route('/pruebas', methods=['GET'])
def show_pruebas():
    # Solo mostrar la página
    return render_template('pruebas.html')

@pruebas.route('/upload', methods=['POST'])
def upload_json():
    # Verificar que el archivo esté presente en la solicitud
    if 'archivo_json' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400

    file = request.files['archivo_json']

    # Asegurarse de que el archivo tenga un nombre (es decir, que no esté vacío)
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
    # Aquí puedes agregar cualquier validación adicional si es necesario.

    # Leer el archivo JSON
    json_content = file.read()

    try:
        data = json.loads(json_content)
    except Exception as e:
        return jsonify({'error': 'Error al analizar el archivo JSON'}), 400

    # Verificar que las claves 'anverso' y 'reverso' estén presentes
    if 'anverso' not in data or 'reverso' not in data:
        return jsonify({'error': 'El archivo JSON no tiene la estructura esperada'}), 400

    # Convertir las imágenes de base64 a objetos de imagen
    anverso=tools.b64_openCV(data['anverso'])
    reverso=tools.b64_openCV(data['reverso'])

    #

    anverso=sift.preparacionInicial(anverso)
    reverso=sift.preparacionInicial(reverso)

    resp_Anverso,resp_reverso=sift.identificador_lados(anverso,reverso)

    #atratapar cuando alguno es falso y generar jSON respuesta
    #aqui se llama a alguna funcion de codeJSON

    resp_Anverso=str(resp_Anverso)
    resp_reverso=str(resp_reverso)

    diccionario_img=cropper.recorte(anverso,reverso)
    clave_omitida=('qr','textoGeneral_MRZ')

    diccionario_ocr = Ocr.obtenerTexto(diccionario_img,*clave_omitida)

    #hacer diccionario MRZ
    dicmrz = {
            "textoGeneral_MRZ": "123",
            "codigoPais_MRZ": "chi", 
                "nombres_MRZ": "juan",
                "RUN_MRZ": "1893",
                "numeroDocumento_MRZ": "5345",
                "apellidos_MRZ": "noi,mbre",
                "nacionalidad_MRZ": "per",
                "sexo_MRZ": "hsudf",
                "fechaNacimiento_MRZ": "1223",
                "fechaVencimiento_MRZ": "23123",
        }


    print('////////////////////////////////')
    carnet=Cedula(diccionario_ocr)
    carnet.mrz['datosMRZ']['textoGeneral_MRZ']=diccionario_ocr['mrz_linea1']+" "+diccionario_ocr['mrz_linea2']+" "+diccionario_ocr['mrz_linea3']
    carnet.actualizar_desde_dicionario(dicmrz)
   
    print('###############################')
    print(carnet.__str__())




    datos_respuesta={
        'ocr_data': vars(carnet),
        'resp_Anverso': resp_Anverso,
        'resp_reverso': resp_reverso
    }
    
    return  jsonify(datos_respuesta)

@pruebas.route('/ocr', methods=['POST'])
def procesar_ocr():
    # Verificar que la imagen esté presente en la solicitud
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400

    image_file = request.files['image']

    # Asegurarse de que la imagen tenga un nombre (es decir, que no esté vacía)
    if image_file.filename == '':
        return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400

    # Convertir la imagen recibida a un formato utilizable para el OCR
    image_data = image_file.read()
    image_data=tools.imagen_a_matriz(image_data)
    dicionario={"imagen":image_data}
    textoCap=Ocr.obtenerTexto(dicionario)
    # Procesar la imagen con la función OCR
    # Asumo que la función Ocr.process() es la que se encarga de esto, si no, reemplázalo por la función adecuada.
  

    # Devolver el texto obtenido
    return textoCap
