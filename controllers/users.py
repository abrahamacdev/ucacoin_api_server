from bottle import request, response
from json import dumps
import re

from model.users_model import *
from logger import Logger


def _validate_email(email):
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)


def _check_new_register_data(data):
    necessary_fields = ['username', 'mail', 'password']

    inside = 0
    for field in data:
        if field in necessary_fields:
            inside += 1

    return inside == len(necessary_fields)


def login():
    json_response = {}
    status_code = 500

    # Falta username o password
    if 'mail' not in request.json or 'password' not in request.json:
        json_response = {
            "msg": 'Falta nombre de usuario o contraseña'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Parseamos el username y el password
    mail = request.json['mail'].strip()
    passwd = request.json['password'].strip()

    # Campo email/password sin nada o email invalido
    if len(mail) == 0 or len(passwd) == 0 or not _validate_email(mail):
        json_response = {
            "msg": 'Usuario o contraseña no válidos'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    try:

        token = login_user(mail, passwd)

        status_code = 200
        json_response = {
            "token": token
        }

    except UserNotExistException as noExistsException:

        status_code = 400
        json_response = {
            "msg": 'Usuario o contraseña no válidos'
        }

    except UserIsLoggedException as loggedException:

        status_code = 400
        json_response = {
            "msg": 'El usuario ya está logueado'
        }

    except Error as error:

        Logger.error(error)

        status_code = 500
        json_response = {
            "msg": 'Error desconocido'
        }

    # Enviamos la respuesta
    response.content_type = 'application/json'
    response.status = status_code
    return dumps(json_response)


def register():
    json_response = {}
    status_code = 500

    # Falta username o password
    if not _check_new_register_data(request.json):
        json_response = {
            "msg": 'Faltan datos'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Parseamos el username y el password
    email = request.json['mail'].strip()
    password = request.json['password'].strip()
    username = request.json['username'].strip()

    # Algún campo no es válido
    if not _validate_email(email) or len(password) == 0 or len(username) == 0:
        json_response = {
            "msg": 'Algún campo no es válido'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Los intentamos registrar en la bd
    try:
        register_new_user(email, username, password)

        status_code = 201
        json_response = {
            "msg": 'Usuario registrado exitósamente'
        }

    except UsersExistsException as userExistsE:

        status_code = 400
        json_response = {
            "msg": 'Ya existe un usuario con esos datos'
        }

    except Error as e:

        status_code = 500
        json_response = {
            "msg": 'Error desconocido'
        }

    # Enviamos la respuesta
    response.content_type = 'application/json'
    response.status = status_code
    return dumps(json_response)


def logout():
    json_response = {}
    status_code = 500

    # Falta token
    if 'token' not in request.json:
        json_response = {
            "msg": 'Token no enviado'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Parseamos el username y el password
    token = request.json['token'].strip()

    # Campo email/password sin nada o email invalido
    if len(token) == 0:
        json_response = {
            "msg": 'Token no valido'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    try:

        # Deslogueamos al usuario
        logout_user(token)

        status_code = 200
        json_response = {
            "msg": 'Se ha desconectado correctamente'
        }

    # El usuario no esta logueado
    except UserNotLoggedException as noLoggedException:

        status_code = 400
        json_response = {
            "msg": 'Error en la peticion'
        }

    except Error as error:

        Logger.error(error)

        status_code = 500
        json_response = {
            "msg": 'Error desconocido'
        }

    # Enviamos la respuesta
    response.content_type = 'application/json'
    response.status = status_code
    return dumps(json_response)
