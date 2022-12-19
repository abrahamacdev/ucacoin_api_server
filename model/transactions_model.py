from sqlite3 import Error
import sqlite3
from hashlib import sha256

from logger import Logger
from exceptions import *
from model import db_manager


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
