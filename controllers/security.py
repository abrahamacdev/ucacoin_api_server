from bottle import request, response
from json import dumps
import re

from exceptions import *
from model import security_model


def check_user_token(token):
    try:

        # Comprobamos que el token del usuario sea válido
        # raise: Error, InvalidTokenException.
        security_model.check_user_token_db(token)
        return True

    except InvalidTokenException as eToken:
        return False

    except Exception as e:
        raise e

def get_user_with_token(token):

    try:

        # Comprobamos que el token del usuario sea válido
        # raise: Error, InvalidTokenException.
        return security_model.get_user_with_token(token)

    except InvalidTokenException as eToken:
        return False

    except Exception as e:
        raise e