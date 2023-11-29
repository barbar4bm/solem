# Utilizar la imagen oficial de Python como imagen base
FROM python:3.11

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Tesseract OCR y sus dependencias
RUN apt-get update \
    && apt-get install -y tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copiar el archivo requirements.txt en el contenedor
COPY requirements.txt ./

# Instalar las dependencias de Python especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de tu código de la aplicación Flask al directorio de trabajo
COPY . .

# Definir la variable de entorno para indicar a Flask cómo ejecutar la aplicación
# Ajustar la ruta para apuntar a app.py dentro de la subcarpeta /app
ENV FLASK_APP=app/app.py


# Exponer el puerto que utiliza Flask, en este caso el 5002
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
