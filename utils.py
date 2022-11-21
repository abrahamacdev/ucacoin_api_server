import os
from enum import Enum
import logging

# SRC_DIR = os.getcwd()

APP_NAME = 'UCA_COIN'

# Directorio raiz del proyecto
ROOT_PATH = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

# Constantes relacionadas con la base de datos
DB_PATH = ROOT_PATH + '/db/'
DB_INITIAL_SCRIPT = DB_PATH + 'db.sqlite'  # Script inicial para la creacion de la estructura de la BD.
DB_NAME = 'ucacoin.db'  # Archivo de la base de datos


#
class __APPMODE(Enum):
    DEV = logging.DEBUG
    PRODUCTION = logging.CRITICAL


# Indica el nivel de depuracion.
__MODE = __APPMODE.DEV
APP_MODE = __MODE.value
