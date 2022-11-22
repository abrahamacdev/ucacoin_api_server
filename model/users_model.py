
from sqlite3 import Error
import sqlite3
from hashlib import sha256

import db_manager
import utils
import constants


def get_login(mail, passwd):

    conn = db_manager.get_conn()

    try:

        # Datos que usaremos para realizar la consulta
        data = [
            (mail, ),
            (passwd, )
        ]

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT email FROM usuario WHERE email = (?) AND passwd = (?)", data)
        email = res.fetchone()
        exists = email is not None

        # Logueamos al usuario
        if exists:
            _loggin(mail)

    except Error as e:
        raise e

def _loggin(mail):

    token = sha256(utils.get_random_string(constants.SECURE_RANDOM_LENGTH).encode('utf-8')).hexdigest()


