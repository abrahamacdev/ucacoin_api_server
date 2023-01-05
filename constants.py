import os
from enum import Enum
import logging

# SRC_DIR = os.getcwd()
# --- Generales ---
APP_NAME = 'UCA_COIN'
SERVER_PORT = 8080          # Puerto en el que nos ejecutaremos
HTTP_PROTOCOL = "http://"
# ------------------





# --- BLockchain core ---
BLOCKCHAIN_API_PORT = 8081  # Puerto en el que está ejecutandose la api de la blockchain
#BLOCKCHAIN_API_IP = "0.0.0.0:"
BLOCKCHAIN_API_IP = "178.62.19.126:"

BLOCKCHAIN_REGISTER_ENDPOINT = "/Register"
BLOCKCHAIN_SEND_COINS_ENDPOINT = "/Transfer"
BLOCKCHAIN_BALANCE_ENDPOINT = "/Balance"
# ------------------------

# ----- Directorios -----
# Directorio raiz del proyecto
ROOT_PATH = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

# Constantes relacionadas con la base de datos
DB_PATH = ROOT_PATH + '/db/'
DB_INITIAL_SCRIPT = DB_PATH + 'db.sqlite'           # Script inicial para la creacion de la estructura de la BD.
DB_FAKE_DATA_SCRIPT = DB_PATH + 'fakeData.sqlite'   # Datos fake para la base de datos (solo en DEV mode)
DB_NAME = 'ucacoin.db'  # Archivo de la base de datos
# -------------------------


# ----- DEBUG -----
class APPMODES(Enum):
    DEV = logging.DEBUG
    PRODUCTION = logging.CRITICAL


# Indica el nivel de depuracion.
APP_MODE = APPMODES.DEV
# -----------------

# ----- Otras -----
SECURE_RANDOM_LENGTH = 16
# -----------------
