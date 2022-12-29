import json
import sqlite3
import requests
from sqlite3 import Error

from constants import *

from logger import Logger

_conn = None


def get_conn():
    global _conn

    if _conn is None:
        raise Exception("La conexión con la base de datos ya se cerró.")

    else:
        return _conn


def close_conn():
    global _conn

    if _conn is None:
        raise Exception("Error al cerrar la conexión.")

    try:
        _conn.close()
        _conn = None

    except Error as e:
        raise e


def initialize_db():
    """
    Comprueba si existe la base de datos. Si no lo está, la crea.
    """

    global _conn

    try:
        _conn = sqlite3.connect(DB_PATH + DB_NAME)

        cursor = _conn.cursor()

        # La tablas no están creadas
        if not _check_tables(_conn):
            Logger.warning("No se creó la estructura de la base de datos.")

            # Creamos las tablas
            _create_db_structure(_conn)

            Logger.info("BD creada")

            # Estamos en desarrollo
            if APP_MODE == APPMODES.DEV:

                # Registramos usuarios de prueba
                _create_example_data(cursor)

                # Registramos a los usuarios en la blockchain
                # TODO Descomentar
                #_register_example_keys(cursor)

                Logger.info("Datos de ejemplo añadidos a la bd")

            # Guardamos los cambios
            _conn.commit()

        Logger.info("BD lista")

    except Exception as e:
        _conn.rollback()                # No guardamos los datos en la bd
        os.remove(DB_PATH + DB_NAME)    # Eliminamos la bd
        Logger.error("Ocurrió un error al inicializar la base de datos")
        Logger.error(e)
        exit(1)


def _check_tables(con):
    cursor = con.cursor()

    try:
        res = cursor.execute("SELECT name FROM sqlite_master")
        tablas_creadas = res.fetchone()
        return tablas_creadas is not None and len(tablas_creadas) > 0

    except Error as e:
        return False


def _create_db_structure(cur):

    try:

        # Leemos el script para crear la base de datos
        with open(DB_INITIAL_SCRIPT) as f:
            script = f.read()

            # Creamos la estructura de la bd
            cur.executescript(script)

    # No se ha podido crear la bd
    except Error as e:

        raise Error("No se han podido crear las tablas")


def _create_example_data(cur):

    with open(DB_FAKE_DATA_SCRIPT) as f:
        script = f.read()

        try:

            # Hacemos las insercciones
            cur.executescript(script)

        except Error as e:
            raise Error("No se han podido añadir los datos de ejemplo a la bd")

def _register_example_keys(cur):

    try:

        # Obtenemos todos los usuarios "pendientes de registro"
        res = cur.execute("SELECT * FROM usuario WHERE clave_privada IS NULL")
        users = res.fetchall()

        url = HTTP_PROTOCOL + BLOCKCHAIN_API_IP + str(BLOCKCHAIN_API_PORT) + BLOCKCHAIN_REGISTER_ENDPOINT

        # Registramos a cada usuario en la blockchain
        for user in users:
            username = user[1]
            body = {
                "username": username
            }

            # Peticion http a la blockchain
            response = requests.get(url, json=body).json()

            # Miramos el codigo de respuesta
            code = response['Code']

            # Le guardamos la clave en la bd
            if code == 201:
                data = (response['private_key'], user[0])

                # Actualizamos la clave privada del usuario en la bd
                cur.execute("UPDATE usuario SET clave_privada = ? WHERE id = ?", data)

            # Ocurrio un error
            else:
                raise Error("No se pudo registrar a los usuarios en la blockchain")

    # Ocurrió un error en la bd
    except Error as e:
        raise e