from flask import Flask
from routes import identity_card


app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>CHECKID -- Solem<h1>"

if __name__ == '__main__': 
    app.register_blueprint(identity_card.identity_card, url_prefix='/identity_card')
    app.run(debug=True,port=5000)
