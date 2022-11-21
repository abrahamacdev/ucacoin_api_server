from bottle import request, response
from json import dumps
import re


def __validar_email(username):
    pattern = re.compile(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    return pattern.match(username)


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
    if len(mail) == 0 or len(passwd) == 0 or not __validar_email(mail):
        json_response = {
            "msg": 'Usuario o contraseña no válidos'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)



    return ""
