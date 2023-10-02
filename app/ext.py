from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


# Este fichero lo utilizaremos para instanciar las distintas extensiones que utilicemos en la aplicación. 
# En este caso, Flask-Marshmallow y Flask-Migrate. El hacerlo aquí evita que se 
# produzcan referencias circulares cuando se utilicen a lo largo de la aplicación
ma = Marshmallow()
migrate = Migrate()