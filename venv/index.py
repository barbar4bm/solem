from config import config
from src import init__app

configuration = config['development']
app = init_app(configuration)

if __name__ = '__main__':
    app.run()