from bottle import request, response
from json import dumps
import re

from model.users_model import *
from model import transactions_model
from logger import Logger
from controllers import security


def _process_balance(user_email, transactions):
    valid_transactions = []

    for transaction in transactions:
        receive_time = transaction[7]

        # No ha recibido la transaccion aun
        if receive_time is None:
            break

        # Transaccion realizada
        else:
            valid_transactions.append(transaction)

    balance = 0.0

    # Si es receptor, aumenta el saldo. Si es emisor, disminuye el saldo
    for valid_transaction in valid_transactions:
        balance += valid_transaction[5] if valid_transaction[4] == user_email else -valid_transaction[5]

    return balance


def _get_balance(email):
    transactions = transactions_model.get_transactions_from_user(email)
    balance = _process_balance(email, transactions)

    return balance


def send():
    json_response = {}
    status_code = 500

    # Faltan datos
    if 'token' not in request.json or 'receptor' not in request.json or 'cantidad' not in request.json:
        json_response = {
            "msg": 'Faltan datos'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Parseamos el token
    token = request.json['token'].strip()
    receptor = request.json['receptor'].strip()
    quantity = 0.0

    # La cantidad tiene que ser un número
    try:
        quantity = float(request.json['cantidad'])

    except Exception as e:
        json_response = {
            "msg": 'Peticion mal formulada'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Comprobamos que el usario esté logueado
    try:
        if not security.check_user_token(token):
            json_response = {
                "msg": 'Token no válido'
            }
            status_code = 400

            response.content_type = 'application/json'
            response.status = status_code
            return dumps(json_response)
    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Obtenemos el correo del usuario a partir del token
    sender_id = ''
    sender_email = ''
    try:
        user = security.get_user_with_token(token)
        sender_email = user[3]
        sender_id = user[0]

    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Obtenemos el id del emisor y receptor
    receiver_id = ''
    try:
        sender_id = get_userid_from_email(sender_email)
        receiver_id = get_userid_from_username(receptor)

    except UserNotExistException as eUser:
        json_response = {
            "msg": 'No existe dicho usuario'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Comprobamos que no se esté intentando enviar dinero a sí mismo
    if receiver_id == sender_id:
        json_response = {
            "msg": 'Mismo emisor y receptor'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code

    # Comprobamos que tenga suficientes fondos
    balance = _get_balance(sender_email)

    """ 
    En caso de que estemos enviando dinero desde la cuenta ROOT y estemos en modo desarrollo, no comprobaremos los fondos
    del emisor (root), en caso contrario comprobamos los fondos de la cuenta
    """
    if constants.APP_MODE == constants.APPMODES.PRODUCTION or (constants.APP_MODE == constants.APPMODES.DEV and sender_id != 1):

        # Quiere enviar más dinero del que tiene
        if balance < quantity:
            json_response = {
                "msg": 'Fondos insuficientes'
            }
            status_code = 400

            response.content_type = 'application/json'
            response.status = status_code
            return dumps(json_response)

    # Creamos la transacción en la base de datos
    try:
        transactions_model.add_new_transaction(quantity, sender_id, receiver_id)

    except Exception as e:
        json_response = {
            "msg": 'Ocurrio un error inesperado'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Devolvemos la creación de la transacción
    status_code = 202

    response.content_type = 'application/json'
    response.status = status_code
    return dumps(json_response)


def actual_balance():
    json_response = {}
    status_code = 500

    # Falta token
    if 'token' not in request.json:
        json_response = {
            "msg": 'Falta el token del usuario'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Parseamos el token
    token = request.json['token'].strip()

    # Comprobamos que el usario esté logueado
    try:
        if not security.check_user_token(token):
            json_response = {
                "msg": 'Token no válido'
            }
            status_code = 400

            response.content_type = 'application/json'
            response.status = status_code
            return dumps(json_response)
    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Obtenemos el correo del usuario a partir del token
    email = ''
    try:
        email = security.get_user_with_token(token)[3]

    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Obtenemos las transacciones del usuario
    balance = _get_balance(email)

    # Las devolvemos
    json_response = {
        "balance": balance
    }
    status_code = 200

    response.content_type = 'application/json'
    response.status = status_code
    return dumps(json_response)

def _filter_history_fields(history):

    final_history = []

    for transaction in history:
        temp = {
            'id': transaction[0],
            'emisor': transaction[1],
            'receptor': transaction[3],
            'cantidad': transaction[5],
            'fecha_envio': transaction[6],
            'fecha_recepcion': transaction[7]
        }

        final_history.append(temp)

    return final_history

def history():
    json_response = {}
    status_code = 500

    # Falta username o password
    if 'token' not in request.json:
        json_response = {
            "msg": 'Falta el token del usuario'
        }
        status_code = 400

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Parseamos el username y el password
    token = request.json['token'].strip()

    # Comprobamos que el usario esté logueado
    try:
        if not security.check_user_token(token):
            json_response = {
                "msg": 'Token no válido'
            }
            status_code = 400

            response.content_type = 'application/json'
            response.status = status_code
            return dumps(json_response)

    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Obtenemos el correo del usuario a partir del token
    email = ''
    try:
        email = security.get_user_with_token(token)[3]

    except Exception as e:
        json_response = {
            "msg": 'Ocurrió un error desconocido'
        }
        status_code = 500

        response.content_type = 'application/json'
        response.status = status_code
        return dumps(json_response)

    # Obtenemos las transacciones del usuario
    transactions = transactions_model.get_transactions_from_user(email)
    transactions = _filter_history_fields(transactions)


    # Las devolvemos
    json_response = {
        "transacciones": transactions
    }
    status_code = 200

    response.content_type = 'application/json'
    response.status = status_code
    return dumps(json_response)
