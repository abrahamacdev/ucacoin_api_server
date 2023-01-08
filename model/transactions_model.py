from sqlite3 import Error
import sqlite3
from hashlib import sha256

import requests

from logger import Logger
from exceptions import *
from model import db_manager, users_model
import constants


def get_transactions_from_user(email):
    conn = db_manager.get_conn()

    try:

        data = (email, email)
        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute('''SELECT t.id 'id', o1.nombre_usuario 'emisor', o1.email, o2.nombre_usuario 'receptor', o2.email, t.cantidad, (CAST(strftime('%s', t.fecha_envio) as integer) * 1000), (CAST(strftime('%s', t.fecha_recepcion) as integer) * 1000) 
                             FROM transaccion as t 
                             INNER JOIN  usuario o1 ON t.id_emisor = o1.id 
                             INNER JOIN usuario o2 ON t.id_receptor = o2.id 
                             WHERE o1.email = ? OR o2.email = ? 
                             ORDER BY t.id ASC''', data)

        return res.fetchall()

    # Ocurrió un error en la bd
    except Error as e:
        raise e

def get_balance(email):

    # Hacemos la peticion
    try:


        user = users_model.get_user_from_email(email)

        # Lo registramos en la blockchain
        body = {
            "username": user[1],
            "private_key": user[4]
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + constants.BLOCKCHAIN_API_IP + str(constants.BLOCKCHAIN_API_PORT) + constants.BLOCKCHAIN_BALANCE_ENDPOINT

        blockchain_response = requests.get(url, json=body).json()

        # Ocurrió un error
        if blockchain_response['Code'] != 200:
            raise Error("Ocurrió un error inesperado")

        # Devolvemos el balance
        else:
            return blockchain_response['balance']

    except Error as e:
        Logger.error(e)
        raise e

def _send_to_blockchain(quantity, sender_username, receiver_username, private_key):
    # Lo registramos en la blockchain
    body = {
        "origin": sender_username,
        "key": private_key,
        "quant": quantity,
        "dest": receiver_username
    }

    # Peticion http a la blockchain
    url = constants.HTTP_PROTOCOL + constants.BLOCKCHAIN_API_IP + str(
        constants.BLOCKCHAIN_API_PORT) + constants.BLOCKCHAIN_SEND_COINS_ENDPOINT

    # Hacemos la peticion
    try:
        blockchain_response = requests.post(url, json=body).json()

        # Se envió el dinero correctamente
        if blockchain_response['Code'] != 202:
            raise BlockchainTransferError("No se pudo transferir la cantidad")

    except Error as e:
        Logger.error(e)
        raise e


def add_new_transaction(quantity, sender_id, receiver_id, sender_username, receiver_username, private_key):
    conn = db_manager.get_conn()

    try:

        # Primero añadimos la transferencia a la blockchain
        _send_to_blockchain(quantity, sender_username, receiver_username, private_key)

        data = (sender_id, receiver_id, quantity)

        cursor = conn.cursor()

        # Creamos al nuevo usuario
        cursor.execute("INSERT INTO transaccion (id_emisor, id_receptor, cantidad) VALUES (?, ?, ?)", data)
        conn.commit()

    # Ocurrió un error en la bd
    except Error as e:
        raise e
