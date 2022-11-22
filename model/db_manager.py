import sqlite3
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

        # La tablas no están creadas
        if not _check_tables(_conn):
            Logger.warning("No se creó la estructura de la base de datos.")

            # Creamos las tablas
            _create_db_structure(_conn)

            Logger.info("BD creada")

            # Estamos en desarrollo
            if APP_MODE == APPMODES.DEV:
                _create_example_data()
                Logger.info("Datos de ejemplo añadidos a la bd")

        Logger.info("BD lista")

    except Exception as e:
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


def _create_db_structure(conn):
    with open(DB_INITIAL_SCRIPT) as f:
        script = f.read()

        consultas = script.split(";")

        # Creamos las tablas
        for consulta in consultas:
            conn.execute(consulta)

    # No se han creado las tablas
    if not _check_tables(conn):
        raise Error("No se han podido crear las tablas")


def _create_example_data():
    global _conn

    with open(DB_FAKE_DATA_SCRIPT) as f:
        script = f.read()

        try:
            cur = _conn.cursor()

            # Hacemos las insercciones
            cur.execute(script)
            _conn.commit()

        except Error as e:
            raise Error("No se han podido añadir los datos de ejemplo a la bd")
