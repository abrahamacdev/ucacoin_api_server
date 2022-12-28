from sqlite3 import Error
import sqlite3
from hashlib import sha256

import requests

from logger import Logger
from exceptions import *
from model import db_manager
import constants


def get_transactions_from_user(email):
    conn = db_manager.get_conn()

    try:

        data = (email, email)
        cursor = conn.cursor()

        # Comprobamos si existe un con dicho email
        res = cursor.execute('''SELECT t.id 'id', o1.nombre_usuario 'emisor', o1.email, o2.nombre_usuario 'receptor', o2.email, t.cantidad, CAST(strftime('%s', t.fecha_envio) as integer), CAST(strftime('%s', t.fecha_recepcion) as integer) 
                             FROM transaccion as t 
                             INNER JOIN  usuario o1 ON t.id_emisor = o1.id 
                             INNER JOIN usuario o2 ON t.id_receptor = o2.id 
                             WHERE o1.email = ? OR o2.email = ? 
                             ORDER BY t.id ASC''', data)

        return res.fetchall()

    # Ocurrió un error en la bd
    except Error as e:
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
