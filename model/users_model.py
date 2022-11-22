from sqlite3 import Error
import sqlite3
from hashlib import sha256

from exceptions import *
import db_manager
import utils
import constants


def get_login(mail, passwd):
    conn = db_manager.get_conn()

    try:

        # Datos que usaremos para realizar la consulta
        data = [
            (mail,),
            (passwd,)
        ]

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT email FROM usuario WHERE email = (?) AND passwd = (?)", data)
        email = res.fetchone()
        exists = email is not None

        # El usuario existe en la bd
        if exists:

            # El usuario ya está logueado
            if _check_user_is_logged(mail):
                raise UserIsLoggedException()

            # Logueamos al usuario
            else:
                return _login(mail)

        # El usuario no existe
        else:
            raise UserNotExistException()

    # Ocurrió un error en la bd
    except Error as e:
        raise e


def _check_user_is_logged(mail):
    """
    Comprueba si un usuario está ya logueado.
    :param mail: COrreo electronico del usuario
    :return: True si el ususario está logueado. False en caso contrario.
    """

    conn = db_manager.get_conn()

    try:

        # Datos que usaremos para realizar la consulta
        data = [
            (mail,),
        ]

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT email FROM login WHERE email = (?)", (mail,))
        email = res.fetchone()
        is_logged = email is not None

        # Logueamos al usuario
        if is_logged:
            return True

        # El usuario no existe
        else:
            return False

    except Error as e:
        raise e


def _login(mail):

    # Generamos el token que devolveremos al usuario
    token = sha256(utils.get_random_string(constants.SECURE_RANDOM_LENGTH).encode('utf-8')).hexdigest()

    conn = db_manager.get_conn()

    try:

        # Datos que usaremos para realizar la consulta
        data = [
            (mail,),
            (token,)
        ]

        cursor = conn.cursor()

        # Guardamos el login
        cursor.execute("INSERT INTO login (email, token) VALUES (?, ?)", data)
        conn.commit()

        return token

    except Error as e:
        raise e
