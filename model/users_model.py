from sqlite3 import Error
import sqlite3
from hashlib import sha256

from logger import Logger
from exceptions import *
from model import db_manager
import utils
import constants

def get_userid_from_username(username):
    conn = db_manager.get_conn()

    try:

        data = (username, )

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT id FROM usuario WHERE nombre_usuario = ?", data)
        res = res.fetchone()

        # No existe ningun usuario con ese nombre de usuario
        if res is None:
            raise UserNotExistException()

        else:
            return res

    # Ocurrió un error en la bd
    except Error as e:
        raise e

def get_userid_from_email(email):
    conn = db_manager.get_conn()

    try:

        data = (email,)

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT id FROM usuario WHERE email = ?", data)
        res = res.fetchone()

        # No existe ningun usuario con ese nombre de usuario
        if res is None:
            raise UserNotExistException()

        else:
            return res

    # Ocurrió un error en la bd
    except Error as e:
        raise e

def register_new_user(email, username, passwd):
    # Comprobamos que no halla un usuario con los mismos datos
    _check_user_exists(email, username)

    # Hasheamos la contrasenia
    hashed_passwd = sha256(passwd.encode('utf-8')).hexdigest()

    # Creamos al usuario
    _create_user(email, username, hashed_passwd)


def _check_user_exists(email, username):
    conn = db_manager.get_conn()

    try:

        data = (email, username)

        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute("SELECT email FROM usuario WHERE email = ? OR nombre_usuario = ?", data)
        email = res.fetchone()
        exists = email is not None

        # Ya existe un usuario en la base de datos con esos datos
        if exists:
            raise UsersExistsException()

    # Ocurrió un error en la bd
    except Error as e:
        raise e


def _create_user(email, username, hashed_passwd):
    conn = db_manager.get_conn()

    try:

        data = (username, hashed_passwd, email)

        cursor = conn.cursor()

        # Creamos al nuevo usuario
        cursor.execute("INSERT INTO usuario (nombre_usuario, passwd_hasheada, email) VALUES (?, ?, ?)", data)
        conn.commit()

    # Ocurrió un error en la bd
    except Error as e:
        raise e

def login_user(email, passwd):
    conn = db_manager.get_conn()

    hashed_passwd = sha256(passwd.encode('utf-8')).hexdigest()

    # Datos que usaremos para realizar la consulta
    data = (email, hashed_passwd,)

    cursor = conn.cursor()

    # Comprobamos si existe un con dicho email
    res = cursor.execute("SELECT email FROM usuario WHERE email = ? AND passwd_hasheada = ?", data)
    exists = res.fetchone() is not None

    # El usuario existe en la bd
    if exists:

        # El usuario ya está logueado
        if _is_user_logged_by_email(email):
            raise UserIsLoggedException()

        # Logueamos al usuario
        else:
            return _login(email)

    # El usuario no existe
    else:
        raise UserNotExistException()

def _is_user_logged_by_email(email):
    """
    Comprueba si un usuario está ya logueado.
    :param email: COrreo electronico del usuario
    :return: True si el ususario está logueado. False en caso contrario.
    :raise Error
    """

    conn = db_manager.get_conn()

    # Datos que usaremos para realizar la consulta
    data = (email,)

    cursor = conn.cursor()

    # Comprobamos si existe un con dicho email
    res = cursor.execute("SELECT email FROM login WHERE email = ?", data)
    return res.fetchone() is not None

def _is_user_logged_by_token(token):
    """
    Comprueba si un usuario está ya logueado.
    :param token: Token devuelto en la etapa de login.
    :return: True si el ususario está logueado. False en caso contrario.
    :raise Error
    """

    conn = db_manager.get_conn()

    # Datos que usaremos para realizar la consulta
    data = (token,)

    cursor = conn.cursor()

    # Comprobamos si existe un con dicho email
    res = cursor.execute("SELECT email FROM login WHERE token = ?", data)

    return res.fetchone() is not None

def _login(mail):
    """
    Loguea a un usuario en la bd.

    :param mail:
    :return:
    :raise Error
    """
    # Generamos el token que devolveremos al usuario
    token = sha256(utils.get_random_string(constants.SECURE_RANDOM_LENGTH).encode('utf-8')).hexdigest()

    conn = db_manager.get_conn()

    # Datos que usaremos para realizar la consulta
    data = (mail, token,)

    cursor = conn.cursor()

    # Guardamos el login
    cursor.execute("INSERT INTO login (email, token) VALUES (?, ?)", data)
    conn.commit()

    return token

def _logout(token):
    """
    Desloguea a un usuario del sistema.

    :param token:
    :return:
    :raise: Error
    """
    conn = db_manager.get_conn()
    cursor = conn.cursor()

    data = (token, )

    cursor.execute("DELETE FROM login WHERE token = ?", data)
    conn.commit()

def logout_user(token):
    """
    Desloguea a un usuario de la bd. Hace alguna comprobacion previa.
    :param token:
    :return:
    :raise: UserNotLoggedExceptio, Error
    """

    # El usuario esta logueado
    if _is_user_logged_by_token(token):
        _logout(token)

    # El usuario no estaba logueado
    else:
        raise UserNotLoggedException()