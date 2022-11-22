import logger
from model.db_manager import *
from controllers.router import *

from logger import Logger

@route('/hello/<name>')
def index(name):
    name + 123
    return template('<b>Hello {{name}}</b>!', name=name)


if __name__ == "__main__":

    # Inicializamos la base de datos
    initialize_db()

    # COnfiguramos el enrutamiento de las peticiones
    #app = setup_routes()

    Logger.info("API en ejecución...")

    # Lanzamos la app
    #run(app, host='localhost', port=8080)
