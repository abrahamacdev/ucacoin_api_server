import sqlite3
from sqlite3 import Error

from utils import *

from logger import Logger


_conn = None


def get_conn():
    return _conn


def check_db():
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

        Logger.info("BD correcta")

    except Exception as e:
        Logger.error("Ocurrió un error al inicializar la base de datos")
        Logger.error(e)
        exit(1)

    finally:
        if _conn:
            _conn.close()


def _check_tables(con):
    cursor = con.cursor()

    try:
        res = cursor.execute("SELECT name FROM sqlite_master")
        tablas_creadas = res.fetchone()
        return tablas_creadas is not None and len(tablas_creadas) > 0

    except Error as e:
        return False


def _create_db_structure(conn):
    with open(DB_PATH + 'db.sqlite') as f:
        script = f.read()

        consultas = script.split(";")

        # Creamos las tablas
        for consulta in consultas:
            conn.execute(consulta)

    # No se han creado las tablas
    if not _check_tables(conn):
        raise Error("No se han podido crear las tablas")
