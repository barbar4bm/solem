# CedulaOCR

API que procesa imágenes de cédulas y extrae información mediante OCR. La API espera recibir imágenes en formato JSON con una estructura específica.
```json
{
  "anverso": "codigo_imagen_base64_anverso",
  "reverso": "codigo_imagen_base64_reverso"
}

## Requisitos

- Python 3.X
- Virtualenv (opcional, pero recomendado).
- Tesseract-OCR instalado en el sistema base y agregado al PATH.

## Instalación y configuración

### 1. Clonar Repositorio

Usa el comando de git para clonar el repositorio en tu máquina local:

```bash
git clone URL_DEL_REPOSITORIO
