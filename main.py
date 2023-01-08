from bottle import run

import constants
import logger
from model.db_manager import *
from controllers.router import *

from logger import Logger

if __name__ == "__main__":

    # Inicializamos la base de datos
    initialize_db()

    # COnfiguramos el enrutamiento de las peticiones
    app = setup_routes()

    Logger.info("API en ejecución...")

    # Lanzamos la app
    run(app, host='0.0.0.0', port=constants.SERVER_PORT)
