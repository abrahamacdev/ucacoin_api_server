from sqlite3 import Error
import sqlite3
from hashlib import sha256

from logger import Logger
from exceptions import *
from model import db_manager
import utils
import constants


def check_user_token_db(token):
    conn = db_manager.get_conn()

    try:

        data = (token,)

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT token FROM login WHERE token = ?", data)
        fetched_token = res.fetchone()
        exists = fetched_token is not None

        # EL usuario NO está logueado en el sistema
        if not exists:
            raise InvalidTokenException()

    # Ocurrió un error en la bd
    except Error as e:
        raise e

def get_user_with_token(token):

    conn = db_manager.get_conn()

    try:

        data = (token,)

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT usuario.* FROM usuario "
                             "INNER JOIN login l ON usuario.email = l.email "
                             "WHERE l.token = ?", data)
        fetched_token = res.fetchone()
        exists = fetched_token is not None

        # EL usuario NO está logueado en el sistema
        if not exists:
            raise InvalidTokenException()

        # Devolvemos el correo del usuario
        return fetched_token

    # Ocurrió un error en la bd
    except Error as e:
        print(e)
        raise e