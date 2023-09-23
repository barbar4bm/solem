from flask import Flask 

#Routes


app = Flask(__name__)

def init__app(config):
    #configuración
    app.config.from_object(config)

    #Blueprints 

    return app