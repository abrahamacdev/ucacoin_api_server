
import unittest

import requests

import constants

TOKEN = "5fd924625f6ab16a19cc9807c7c506ae1813490e4ba675f843d5a10e0baacdb8"
PRIVATE_KEY = "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc"

SERVER_IP = constants.BLOCKCHAIN_API_IP

class TransactionsIntegrationTests(unittest.TestCase):

    def test_cannot_send_more_than_i_have(self):
        """
        Comprobamos que no se pueda enviar más dinero del que dispone el usuario.
        Partimos de:
            * Token de usuario logueado válido
            * Receptor existente
            * Cantidad INVALIDA

        El resultdo esperado es un código de error (HTTP Status Code) 500
        """

        # Lo registramos en la blockchain
        body = {
            "token": TOKEN,
            "receptor": "pepito",
            "cantidad": 99999999999999999.0
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + SERVER_IP + str(constants.SERVER_PORT) + "/enviar"

        try:
            response = requests.post(url, json=body)

            self.assertEqual(response.status_code, 500)

        except Exception as e:
            self.assertTrue(False)


    def test_cannot_send_to_inexistent_user(self):
        """
        Comprobamos que no se pueda enviar dinero a un usuario no registrado en el sistema.
        Partimos de:
            * Token de usuario logueado válido
            * Receptor INEXISTENTE
            * Cantidad valida

        El resultdo esperado es un código de error (HTTP Status Code) 400
        """

        # Lo registramos en la blockchain
        body = {
            "token": TOKEN,
            "receptor": "xxtentation",
            "cantidad": 10.0
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + SERVER_IP + str(constants.SERVER_PORT) + "/enviar"

        try:
            response = requests.post(url, json=body)

            self.assertEqual(response.status_code, 400)

        except Exception as e:
            self.assertTrue(False)


    def test_cannot_send_negative_quantity(self):
        """
        Comprobamos que no se pueda enviar una cantidad de dinero negativa.
        Partimos de:
            * Token de usuario logueado válido
            * Receptor existente
            * Cantidad NEGATIVA

        El resultdo esperado es un código de error (HTTP Status Code) 400
        """

        # Lo registramos en la blockchain
        body = {
            "token": TOKEN,
            "receptor": "pepito",
            "cantidad": -10.0
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + SERVER_IP + str(constants.SERVER_PORT) + "/enviar"

        try:
            response = requests.post(url, json=body)

            self.assertEqual(response.status_code, 400)

        except Exception as e:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()