# CedulaOCR

API que procesa imágenes de cédulas de identidad y extrae su información mediante OCR. La API espera recibir dos imágenes (anverso, reverso) encapsuladas en formato JSON, con una estructura específica. 
La imagen debe venir codificada en cadena de caracteres en base 64


```plaintext
9j/4AAQSk...
```
### Estructura del JSON
```json
{
  "anverso": "9j/4AAQSk...",
  "reverso": "codigo_imagen_base64_reverso"
}

```

## Requisitos

- Python 3.X
- Virtualenv (opcional, pero recomendado).
- Tesseract-OCR instalado en el sistema base y agregado al PATH.

## Instalación y configuración

### 1. Clonar Repositorio
### 2. Activar entorno virtual (venv "Virtual Environment") ejecutando "app.py"
### 3. Visitar servidor http://127.0.0.1:5000 escoger la ruta de prueba http://127.0.0.1:5000/pruebas

